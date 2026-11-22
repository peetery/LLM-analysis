import io
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from automation.verified_qwen import (
    GEMINI_MODEL,
    MODEL,
    apply_response,
    digest,
    feedback_prompt,
    load_qwen_suite,
    inspect_suite,
    quality_passed,
    run_verified,
    source_branches,
    worker,
)


class TestVerifiedQwen(unittest.TestCase):
    SOURCE = "def double(value):\n    return value * 2\n"
    SUITE = (
        "import unittest\nfrom example import double\n"
        "class Tests(unittest.TestCase):\n"
        "    def test_double(self):\n"
        "        self.assertEqual(double(3), 6)\n"
    )

    def pool(self, source, *_args):
        mutants = [
            {
                "id": str(index),
                "source": f"return value * {index + 3}",
                "sha256": digest(f"return value * {index + 3}"),
                "split": split,
                "start_line": index + 1,
                "diff": f"DEVELOPMENT_{index}",
            }
            for index, split in enumerate(("development", "heldout"))
        ]
        return {"source_sha256": digest(source), "mutants": mutants}

    def execute(self, source, tests, module, coverage=False, freeze=False):
        return {
            "status": "passed" if coverage else "failed",
            "tests": 1,
            "failures": 0,
            "errors": 0,
            "skipped": 0,
            "branch_coverage": 98.5,
            "log": "",
            "missing_lines": [],
            "missing_branches": [],
        }

    def test_exact_mutation_threshold_is_not_accepted(self):
        baseline = {"status": "passed", "tests": 1, "skipped": 0, "branch_coverage": 98}
        outcomes = [{"outcome": "killed"}] * 3 + [{"outcome": "survived"}] * 2
        self.assertFalse(quality_passed(baseline, outcomes, 60, 98))
        self.assertTrue(quality_passed(baseline, [{"outcome": "killed"}], 60, 98))
        for change in (
            {"status": "failed"},
            {"tests": 0},
            {"branch_coverage": 97.99},
            {"skipped": 1},
        ):
            self.assertFalse(
                quality_passed({**baseline, **change}, [{"outcome": "killed"}], 60, 98)
            )

    def test_unchanged_qualified_suite_is_revalidated_without_loading_a_key(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_file = root / "example.py"
            source_file.write_text(self.SOURCE)
            client = Mock(provider_calls=[], send_prompt=Mock(return_value=self.SUITE))
            factory = Mock(return_value=client)
            with (
                patch("automation.verified_qwen.frozen_pool", side_effect=self.pool),
                patch("automation.verified_qwen.worker", side_effect=self.execute),
                patch("automation.verified_qwen.environment", return_value={"version": 1}),
            ):
                first = run_verified(source_file, root / "results", root / "cache", factory)
                forbidden = Mock(
                    side_effect=AssertionError("Cache hit must not request credentials")
                )
                second = run_verified(source_file, root / "results", root / "cache", forbidden)
                fresh = run_verified(
                    source_file, root / "results", root / "cache", factory, fresh=True
                )
            self.assertTrue(first["quality_passed"])
            self.assertTrue(second["cache_hit"])
            self.assertEqual(second["model_requests_this_run"], 0)
            self.assertEqual(second["mutation_score"], first["mutation_score"])
            self.assertFalse(fresh["cache_hit"])
            self.assertEqual(fresh["model_requests_this_run"], 1)
            self.assertEqual(factory.call_count, 2)
            forbidden.assert_not_called()

    def test_google_generation_keeps_cache_and_lineage_separate_from_qwen(self):
        from automation.cli_automation.gemini_api_client import GeminiAPIClient

        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_file = root / "example.py"
            source_file.write_text(self.SOURCE)
            qwen = Mock(
                model=MODEL,
                provider_calls=[{"model": MODEL, "finish_reason": "stop"}],
                send_prompt=Mock(return_value=self.SUITE),
            )
            response = {
                "modelVersion": GEMINI_MODEL,
                "candidates": [
                    {"finishReason": "STOP", "content": {"parts": [{"text": self.SUITE}]}}
                ],
            }
            with (
                patch("automation.verified_qwen.frozen_pool", side_effect=self.pool),
                patch("automation.verified_qwen.worker", side_effect=self.execute),
                patch("automation.verified_qwen.environment", return_value={"version": 1}),
                patch(
                    "automation.cli_automation.gemini_api_client.urlopen",
                    return_value=io.BytesIO(("data: " + json.dumps(response) + "\n\n").encode()),
                ) as transport,
            ):
                previous = run_verified(source_file, root / "results", root / "cache", lambda: qwen)
                google = run_verified(
                    source_file,
                    root / "results",
                    root / "cache",
                    lambda: GeminiAPIClient(api_key="fixture-google-key"),
                    model=GEMINI_MODEL,
                )
                forbidden = Mock(side_effect=AssertionError("Cache must not ask for a key"))
                cached = run_verified(
                    source_file,
                    root / "results",
                    root / "cache",
                    forbidden,
                    model=GEMINI_MODEL,
                )
                rejected = run_verified(
                    source_file,
                    root / "results",
                    root / "cache",
                    lambda: qwen,
                    model=GEMINI_MODEL,
                    fresh=True,
                )
            self.assertTrue(google["quality_passed"])
            self.assertFalse(google["cache_hit"])
            self.assertEqual(google["provider"], "google")
            self.assertEqual(google["provenance"][0]["origin"], "gemini_generation")
            self.assertTrue(cached["cache_hit"])
            forbidden.assert_not_called()
            self.assertEqual(transport.call_count, 1)
            self.assertTrue(
                transport.call_args.args[0].full_url.startswith(
                    "https://generativelanguage.googleapis.com/"
                )
            )
            self.assertEqual(rejected["model_requests_this_run"], 0)
            self.assertIn("Client model differs", rejected["error"])
            suite, _ = load_qwen_suite(
                google["result_dir"], self.SOURCE, "example", model=GEMINI_MODEL
            )
            self.assertEqual(suite, self.SUITE)
            with self.assertRaises(ValueError):
                load_qwen_suite(previous["result_dir"], self.SOURCE, "example", model=GEMINI_MODEL)

    def test_source_environment_targets_and_suite_tampering_invalidate_cache(self):
        for change in ("source", "environment", "target", "tests"):
            with self.subTest(change=change), TemporaryDirectory() as directory:
                root = Path(directory)
                source_file = root / "example.py"
                source_file.write_text(self.SOURCE)
                client = Mock(provider_calls=[], send_prompt=Mock(return_value=self.SUITE))
                factory = Mock(return_value=client)
                current_environment = {"version": 1}
                with (
                    patch("automation.verified_qwen.frozen_pool", side_effect=self.pool),
                    patch("automation.verified_qwen.worker", side_effect=self.execute),
                    patch(
                        "automation.verified_qwen.environment",
                        side_effect=lambda: dict(current_environment),
                    ),
                ):
                    run_verified(source_file, root / "results", root / "cache", factory)
                    target = 60
                    if change == "source":
                        source_file.write_text(self.SOURCE + "# Changed source\n")
                    elif change == "environment":
                        current_environment["version"] = 2
                    elif change == "target":
                        target = 61
                    else:
                        entry = next((root / "cache/entries").glob("*.json"))
                        data = json.loads(entry.read_text())
                        data["tests"] += "\n# Tampered suite\n"
                        entry.write_text(json.dumps(data))
                    report = run_verified(
                        source_file,
                        root / "results",
                        root / "cache",
                        factory,
                        mutation_target=target,
                    )
                self.assertFalse(report["cache_hit"])
                self.assertEqual(factory.call_count, 2)

    def test_low_scores_are_blocked_and_not_cached(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_file = root / "example.py"
            source_file.write_text(self.SOURCE)
            client = Mock(provider_calls=[], send_prompt=Mock(return_value=self.SUITE))
            with (
                patch("automation.verified_qwen.frozen_pool", side_effect=self.pool),
                patch("automation.verified_qwen.worker", side_effect=self.execute),
                patch("automation.verified_qwen.environment", return_value={}),
                patch(
                    "automation.verified_qwen.mutation_results",
                    side_effect=lambda tests, mutants, module: [
                        {"id": item["id"], "outcome": "survived"} for item in mutants
                    ],
                ),
            ):
                report = run_verified(
                    source_file, root / "results", root / "cache", lambda: client, max_refinements=0
                )
            self.assertFalse(report["quality_passed"])
            self.assertEqual(report["status"], "blocked")
            self.assertEqual(list((root / "cache/entries").glob("*.json")), [])

    def test_bounded_feedback_improves_development_score_without_exposing_heldout(self):
        additions = json.dumps(
            {
                "edits": [],
                "additions": "class Extra(unittest.TestCase):\n"
                "    def test_zero(self):\n        self.assertEqual(double(0), 0)\n",
            }
        )
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_file = root / "example.py"
            source_file.write_text(self.SOURCE)
            client = Mock(
                provider_calls=[],
                send_prompt=Mock(side_effect=[self.SUITE, '{"edits":', additions]),
            )

            def mutation_outcomes(tests, mutants, module):
                return [
                    {
                        "id": item["id"],
                        "outcome": "killed" if "class Extra" in tests else "survived",
                    }
                    for item in mutants
                ]

            with (
                patch("automation.verified_qwen.frozen_pool", side_effect=self.pool),
                patch("automation.verified_qwen.worker", side_effect=self.execute),
                patch("automation.verified_qwen.environment", return_value={}),
                patch("automation.verified_qwen.mutation_results", side_effect=mutation_outcomes),
            ):
                report = run_verified(source_file, root / "results", root / "cache", lambda: client)
            self.assertTrue(report["quality_passed"])
            self.assertEqual(client.send_prompt.call_count, 3)
            final_prompt = client.send_prompt.call_args.args[0]
            self.assertIn("DEVELOPMENT_0", final_prompt)
            self.assertNotIn("DEVELOPMENT_1", final_prompt)
            self.assertIn("PREVIOUS REJECTED CANDIDATE FEEDBACK", final_prompt)
            self.assertIn("Expecting", final_prompt)
            final_suite = (Path(report["result_dir"]) / "tests.py").read_text()
            self.assertIn(self.SUITE.rstrip(), final_suite)
            self.assertIn("class Extra", final_suite)

    def test_additions_preserve_existing_assertions_and_feedback_excludes_heldout(self):
        response = json.dumps(
            {
                "edits": [],
                "additions": "class Extra(unittest.TestCase):\n"
                "    def test_zero(self):\n        self.assertEqual(double(0), 0)\n",
            }
        )
        candidate, repairs = apply_response(self.SUITE, response, "", "example")
        fenced_candidate, _ = apply_response(self.SUITE, response + "\n```", "", "example")
        self.assertEqual(fenced_candidate, candidate)
        for extra in ('\n{"edits": [], "additions": ""}', "\nIgnore the original tests."):
            with (
                self.subTest(extra=extra),
                self.assertRaisesRegex(ValueError, "Unexpected content"),
            ):
                apply_response(self.SUITE, response + extra, "", "example")
        self.assertIn(self.SUITE.rstrip(), candidate)
        self.assertEqual(repairs, [])
        changed = json.dumps(
            {
                "edits": [
                    {
                        "old": "self.assertEqual(double(3), 6)",
                        "new": "self.assertEqual(double(3), 9)",
                        "reason": "wrong oracle",
                    }
                ],
                "additions": "",
            }
        )
        with self.assertRaises(ValueError):
            apply_response(self.SUITE, changed, "", "example")
        pool = self.pool(self.SOURCE)["mutants"]
        prompt = feedback_prompt(
            self.SOURCE, self.SUITE, {}, [pool[0]], [{"id": "0", "outcome": "survived"}]
        )
        self.assertIn("DEVELOPMENT_0", prompt)
        self.assertNotIn("DEVELOPMENT_1", prompt)
        for additions in (
            "from unittest import TestCase as double\n",
            "class double(unittest.TestCase):\n    pass\n",
            "from unittest import expectedFailure as allowed\n",
        ):
            with self.subTest(additions=additions), self.assertRaises(ValueError):
                apply_response(
                    self.SUITE, json.dumps({"edits": [], "additions": additions}), "", "example"
                )

    def test_feedback_targets_the_exact_missing_argument_guard(self):
        source = (
            "def calculate(value, discount):\n"
            "    if not isinstance(value, (int, float)):\n"
            "        raise TypeError('Value must be a number.')\n"
            "    if not isinstance(discount, (int, float)):\n"
            "        raise TypeError('Discount must be a number.')\n"
            "    return value * (1 - discount)\n"
        )
        branches = source_branches(source, [[4, 5]])
        self.assertEqual(len(branches), 1)
        self.assertEqual(branches[0]["method"], "calculate")
        self.assertIn("discount", branches[0]["condition"])
        self.assertIn("Discount must be a number.", branches[0]["true_path"])
        prompt = feedback_prompt(
            source, self.SUITE, {"status": "passed", "missing_branches": [[4, 5]]}, [], []
        )
        priority = prompt.split("MISSING BRANCH TARGETS", 1)[1].split("\nSOURCE:", 1)[0]
        self.assertIn("Discount must be a number.", priority)
        self.assertNotIn("Value must be a number.", priority)

    def test_addition_lists_are_normalized_without_changing_code_or_lifting_guards(self):
        addition = (
            "class Extra(unittest.TestCase):\n"
            "    def test_zero(self):\n        self.assertEqual(double(0), 0)\n"
        )
        candidate, _ = apply_response(
            self.SUITE, json.dumps({"edits": [], "additions": [addition]}), "", "example"
        )
        self.assertEqual(candidate, self.SUITE.rstrip() + "\n\n" + addition)
        with self.assertRaisesRegex(ValueError, "list of Python text"):
            apply_response(
                self.SUITE, json.dumps({"edits": [], "additions": [addition, 3]}), "", "example"
            )
        too_many = "class Extra(unittest.TestCase):\n" + "".join(
            f"    def test_{index}(self):\n        self.assertEqual(double(0), 0)\n"
            for index in range(17)
        )
        with self.assertRaisesRegex(ValueError, "sixteen"):
            apply_response(
                self.SUITE, json.dumps({"edits": [], "additions": [too_many]}), "", "example"
            )
        unwanted_edit = {
            "old": "self.assertEqual(double(3), 6)",
            "new": "self.assertEqual(double(3), 9)",
            "reason": "Unnecessary change to a passing expectation.",
        }
        recovered, repairs = apply_response(
            self.SUITE,
            json.dumps({"edits": [unwanted_edit], "additions": too_many}),
            "",
            "example",
            additions_only=True,
        )
        self.assertEqual(repairs, [])
        self.assertTrue(recovered.startswith(self.SUITE.rstrip() + "\n\n"))
        self.assertIn("def test_16", recovered)
        with self.assertRaisesRegex(ValueError, "thirty-two"):
            apply_response(
                self.SUITE,
                json.dumps(
                    {
                        "edits": [],
                        "additions": too_many
                        + "".join(
                            f"    def test_{index}(self):\n        self.assertEqual(double(0), 0)\n"
                            for index in range(17, 33)
                        ),
                    }
                ),
                "",
                "example",
                additions_only=True,
            )

    def test_saved_qwen_feedback_can_qualify_without_any_new_model_requests(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_file = root / "example.py"
            source_file.write_text(self.SOURCE)
            bad_suite = self.SUITE.replace("double(3), 6", "double(3), 9")
            archive = root / "archive"
            archive.mkdir()
            (archive / "example.py").write_text(self.SOURCE)
            (archive / "tests.py").write_text(bad_suite)
            provider_calls = [
                {"model": "qwen/qwen3-coder-30b-a3b-instruct", "finish_reason": "stop"}
            ]
            (archive / "experiment_results.json").write_text(
                json.dumps(
                    {"raw_results": {"response": bad_suite, "provider_calls": provider_calls}}
                )
            )
            blocked = root / "blocked"
            round_dir = blocked / "round_1"
            round_dir.mkdir(parents=True)
            (blocked / "config.json").write_text(
                json.dumps(
                    {
                        "source_sha256": digest(self.SOURCE),
                        "pool_sha256": digest(self.pool(self.SOURCE)),
                    }
                )
            )
            (blocked / "report.json").write_text(
                json.dumps({"provenance": [{"original_run": str(archive)}]})
            )
            (round_dir / "request.json").write_text(
                json.dumps(
                    {"prompt": f"SOURCE:\n{self.SOURCE}\nCURRENT SUITE:\n{bad_suite}\n\nEXECUTION:"}
                )
            )
            content = json.dumps(
                {
                    "edits": [
                        {
                            "old": "self.assertEqual(double(3), 9)",
                            "new": "self.assertEqual(double(3), 6)",
                            "reason": "Source returns value * 2, so 3 * 2 = 6.",
                        }
                    ],
                    "additions": [
                        "class Extra(unittest.TestCase):\n"
                        "    def test_zero(self):\n        self.assertEqual(double(0), 0)\n"
                    ],
                }
            )
            (round_dir / "response.json").write_text(
                json.dumps({"content": content, "provider_calls": provider_calls})
            )

            def execute(source, tests, module, coverage=False, freeze=False):
                result = self.execute(source, tests, module, coverage, freeze)
                if coverage and "double(3), 9" in tests:
                    result.update(
                        status="failed", log='File "/saved/tests.py", line 5, in test_double\n'
                    )
                return result

            forbidden = Mock(
                side_effect=AssertionError("Saved response replay must not load credentials")
            )
            with (
                patch("automation.verified_qwen.frozen_pool", side_effect=self.pool),
                patch("automation.verified_qwen.worker", side_effect=execute),
                patch("automation.verified_qwen.environment", return_value={}),
            ):
                report = run_verified(
                    source_file, root / "results", root / "cache", forbidden, replay_from=blocked
                )
                admitted, lineage = load_qwen_suite(report["result_dir"], self.SOURCE, "example")
                repeated = run_verified(source_file, root / "results", root / "cache", forbidden)
            self.assertTrue(report["quality_passed"])
            self.assertEqual(admitted, self.SUITE)
            self.assertEqual(lineage[-1]["tests_sha256"], digest(admitted))
            self.assertEqual(report["model_requests_this_run"], 0)
            self.assertEqual(report["replayed_responses_this_run"], 1)
            self.assertTrue(repeated["cache_hit"])
            self.assertEqual(repeated["replayed_responses_this_run"], 0)
            self.assertEqual((archive / "tests.py").read_text(), bad_suite)
            forbidden.assert_not_called()
            saved = Path(report["result_dir"]) / "tests.py"
            saved.write_text(admitted + "\n# External modification\n")
            with self.assertRaisesRegex(ValueError, "modified outside Qwen admission"):
                load_qwen_suite(report["result_dir"], self.SOURCE, "example")

    def test_repair_phase_preserves_original_tests_and_rejects_all_additions(self):
        wrong = self.SUITE.replace("double(3), 6", "double(3), 9")
        response = json.dumps(
            {
                "edits": [
                    {
                        "old": "self.assertEqual(double(3), 9)",
                        "new": "self.assertEqual(double(3), 6)",
                        "reason": "Source returns 3 * 2 = 6.",
                    }
                ],
                "additions": "class Bad(unittest.TestCase):\n"
                "    def test_wrong(self):\n        self.assertEqual(double(1), -1)\n",
            }
        )
        log = 'File "/tmp/tests.py", line 5, in test_double\n'
        candidate, repairs = apply_response(wrong, response, log, "example", repairs_only=True)
        self.assertEqual(candidate, self.SUITE)
        self.assertEqual(len(repairs), 1)
        self.assertEqual(worker(self.SOURCE, candidate, "example")["status"], "passed")
        with self.assertRaisesRegex(ValueError, "reported failing"):
            apply_response(wrong, response, "", "example", repairs_only=True)
        prompt = feedback_prompt(self.SOURCE, wrong, {"status": "failed", "log": log}, [], [])
        self.assertIn("REPAIR-ONLY PHASE", prompt)
        self.assertNotIn("MISSING BRANCH TARGETS", prompt)
        self.assertNotIn("DEVELOPMENT MUTANT CHALLENGES", prompt)

    def test_source_instance_state_cannot_force_unreachable_coverage(self):
        prefix = (
            "import unittest\nfrom example import Cart\n"
            "class Tests(unittest.TestCase):\n"
            "    def test_cart(self):\n        cart = Cart()\n"
        )
        inspect_suite(
            prefix + "        cart.add_item('Apple', 1, 1)\n"
            "        self.assertEqual(cart.get_subtotal(), 1)\n",
            "example",
        )
        for operation in (
            "cart.items = []",
            "cart.items[0]['price'] = -1",
            "alias = cart\n        alias.items.clear()",
            "cart._validate_amount(1)",
        ):
            with self.subTest(operation=operation), self.assertRaises(ValueError):
                inspect_suite(prefix + "        " + operation + "\n", "example")

    def test_isolated_worker_measures_real_execution_and_freezes_disjoint_regions(self):
        source = (
            "def double(value):\n"
            "    if value < 0:\n"
            "        raise ValueError('negative')\n"
            "    return value * 2\n"
        )
        report = worker(source, self.SUITE, "example", coverage=True)
        self.assertEqual(report["status"], "passed", report.get("log"))
        self.assertGreater(report["branch_coverage"], 0)
        pool = worker(source, None, "example", freeze=True)
        self.assertIn("mutants", pool, pool.get("log"))
        dev_lines = set()
        heldout_lines = set()
        for item in pool["mutants"]:
            lines = dev_lines if item["split"] == "development" else heldout_lines
            lines.update(range(item["start_line"], item["end_line"] + 1))
        self.assertTrue(dev_lines)
        self.assertTrue(heldout_lines)
        self.assertFalse(dev_lines & heldout_lines)

    def test_verified_continuation_preserves_lineage_and_limits_new_requests(self):
        calls = [{"model": "qwen/qwen3-coder-30b-a3b-instruct", "finish_reason": "stop"}]
        addition = json.dumps(
            {
                "edits": [
                    {
                        "old": "self.assertEqual(double(3), 6)",
                        "new": "self.assertEqual(double(3), 9)",
                        "reason": "Unwanted edit to a passing test.",
                    }
                ],
                "additions": "class Extra(unittest.TestCase):\n"
                "    def test_zero(self):\n        self.assertEqual(double(0), 0)\n",
            }
        )
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_file = root / "example.py"
            source_file.write_text(self.SOURCE)
            initial_client = Mock(provider_calls=calls, send_prompt=Mock(return_value=self.SUITE))
            next_client = Mock(provider_calls=calls, send_prompt=Mock(return_value=addition))
            forbidden = Mock(side_effect=AssertionError("Do not regenerate or request credentials"))

            def outcomes(tests, mutants, module):
                return [
                    {
                        "id": item["id"],
                        "outcome": "killed" if "class Extra" in tests else "survived",
                    }
                    for item in mutants
                ]

            with (
                patch("automation.verified_qwen.frozen_pool", side_effect=self.pool),
                patch("automation.verified_qwen.worker", side_effect=self.execute),
                patch("automation.verified_qwen.mutation_results", side_effect=outcomes),
                patch("automation.verified_qwen.environment", return_value={}),
            ):
                initial = run_verified(
                    source_file,
                    root / "results",
                    root / "cache",
                    lambda: initial_client,
                    max_refinements=0,
                )
                continued = run_verified(
                    source_file,
                    root / "results",
                    root / "cache",
                    lambda: next_client,
                    resume_from=initial["result_dir"],
                    max_refinements=1,
                )
                reconstructed = run_verified(
                    source_file,
                    root / "results",
                    root / "other_cache",
                    forbidden,
                    resume_from=continued["result_dir"],
                    max_refinements=0,
                )
            self.assertFalse(initial["quality_passed"])
            self.assertTrue(continued["quality_passed"])
            self.assertTrue(reconstructed["quality_passed"])
            self.assertEqual(next_client.send_prompt.call_count, 1)
            self.assertEqual(continued["model_requests_this_run"], 1)
            self.assertEqual(reconstructed["model_requests_this_run"], 0)
            admission = json.loads(
                (Path(continued["result_dir"]) / "round_1/admission.json").read_text()
            )
            self.assertTrue(admission["additions_only"])
            self.assertEqual(len(admission["rejected_edits"]), 1)
            self.assertIn(self.SUITE.rstrip(), next_client.send_prompt.call_args.args[0])
            forbidden.assert_not_called()
            admitted, lineage = load_qwen_suite(continued["result_dir"], self.SOURCE, "example")
            self.assertTrue(admitted.startswith(self.SUITE.rstrip() + "\n\n"))
            self.assertEqual((Path(reconstructed["result_dir"]) / "tests.py").read_text(), admitted)
            for kind in ("response", "request", "source"):
                with self.subTest(kind=kind):
                    if kind == "source":
                        target = Path(continued["result_dir"]) / "example.py"
                    else:
                        target = Path(lineage[-1][kind + "_file"])
                    saved = target.read_text()
                    if kind == "response":
                        data = json.loads(saved)
                        data["content"] = addition.replace("double(0), 0", "double(0), 1")
                        target.write_text(json.dumps(data))
                    elif kind == "request":
                        data = json.loads(saved)
                        data["prompt"] = data["prompt"].replace("double(3), 6", "double(3), 5")
                        target.write_text(json.dumps(data))
                    else:
                        target.write_text(saved + "# Changed source\n")
                    try:
                        with self.assertRaises(ValueError):
                            load_qwen_suite(continued["result_dir"], self.SOURCE, "example")
                    finally:
                        target.write_text(saved)

    def test_manually_modified_archive_cannot_be_claimed_as_qwen_generation(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_file = root / "example.py"
            source_file.write_text(self.SOURCE)
            archive = root / "archive"
            archive.mkdir()
            (archive / "example.py").write_text(self.SOURCE)
            (archive / "tests.py").write_text(self.SUITE.replace("double(3), 6", "double(3), 9"))
            (archive / "experiment_results.json").write_text(
                json.dumps(
                    {
                        "raw_results": {
                            "response": self.SUITE,
                            "provider_calls": [
                                {
                                    "model": "qwen/qwen3-coder-30b-a3b-instruct",
                                    "finish_reason": "stop",
                                }
                            ],
                        }
                    }
                )
            )
            factory = Mock(
                side_effect=AssertionError("Do not request a key for an invalid archive")
            )
            with (
                patch("automation.verified_qwen.frozen_pool", side_effect=self.pool),
                patch("automation.verified_qwen.environment", return_value={}),
            ):
                result = run_verified(
                    source_file, root / "results", root / "cache", factory, resume_from=archive
                )
            self.assertEqual(result["status"], "blocked")
            self.assertIn("Archived tests differ", result["error"])
            factory.assert_not_called()

    def test_real_cli_cache_hit_needs_no_key_even_with_prompt_key_flag(self):
        project = Path(__file__).parents[1]
        source = (
            "def double(value):\n"
            "    if value < 0:\n        raise ValueError('negative')\n"
            "    return value * 2\n"
        )
        suite = self.SUITE + (
            "    def test_negative(self):\n"
            "        with self.assertRaises(ValueError) as caught:\n"
            "            double(-1)\n"
            "        self.assertEqual(str(caught.exception), 'negative')\n"
        )
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_file = root / "example.py"
            source_file.write_text(source)
            arguments = [
                "cli_experiment_runner.py",
                "--model",
                "qwen3-coder-30b",
                "--source-file",
                str(source_file),
                "--context",
                "full_context",
                "--strategy",
                "simple_prompting",
                "--verified-cache",
                "--results-dir",
                str(root / "results"),
                "--cache-dir",
                str(root / "cache"),
            ]
            script = (
                "import runpy, sys\nfrom unittest.mock import patch\n"
                f"sys.path.insert(0, {str(project / 'automation')!r})\n"
                f"sys.argv = {arguments!r}\n"
                "with patch('cli_automation.qwen_client.QwenClient.send_prompt', "
                f"return_value={suite!r}):\n"
                f"    runpy.run_path({str(project / 'automation/cli_experiment_runner.py')!r}, "
                "run_name='__main__')\n"
            )
            first = subprocess.run(
                [sys.executable, "-c", script],
                cwd=root,
                env={**os.environ, "OPENROUTER_API_KEY": "fixture-secret"},
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            env = {key: value for key, value in os.environ.items() if key != "OPENROUTER_API_KEY"}
            repeated = subprocess.run(
                [
                    sys.executable,
                    str(project / "automation/cli_experiment_runner.py"),
                    *arguments[1:],
                    "--prompt-key",
                ],
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(repeated.returncode, 0, repeated.stdout + repeated.stderr)
            self.assertIn("Verified cache hit", repeated.stdout)
            self.assertIn('"model_requests_this_run": 0', repeated.stdout)
            self.assertNotIn("API key (hidden)", repeated.stdout + repeated.stderr)


if __name__ == "__main__":
    unittest.main()
