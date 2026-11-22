import json
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from automation.experiment_runner import ExperimentRunner
from automation.suite_refinement import refine_failed_suite, validated_numeric_edits


class TestSuiteRefinement(unittest.TestCase):
    INITIAL = (
        "import unittest\n"
        "class Tests(unittest.TestCase):\n"
        "    def test_total(self):\n"
        "        result = 25.2\n"
        "        self.assertEqual(result, 13.2)\n"
    )
    FAILURE = 'File "/saved/tests.py", line 5, in test_total\nAssertionError: total\n'

    def edits(self, old="self.assertEqual(result, 13.2)", new="self.assertEqual(result, 25.2)"):
        return json.dumps({"edits": [{
            "old": old, "new": new,
            "reason": "(11 subtotal + 10 shipping) * 1.2 = 25.2"
        }]})

    def test_numeric_repair_preserves_inputs_and_requires_audit(self):
        candidate, repairs, _ = validated_numeric_edits(self.INITIAL, self.edits(), self.FAILURE)
        self.assertEqual(candidate, self.INITIAL.replace("13.2", "25.2"))
        self.assertEqual(repairs[0]["expected_before"], 13.2)
        self.assertEqual(repairs[0]["expected_after"], 25.2)
        self.assertEqual(repairs[0]["review_status"], "pending")

    def test_unsupported_changes_or_unreported_assertions_are_rejected(self):
        responses = [
            self.edits("result = 25.2", "result = 13.2"),
            self.edits(new="self.assertEqual(25.2, 25.2)"),
            self.edits(new="self.assertAlmostEqual(result, 25.2)"),
            self.edits(new="self.assertEqual(result, result)"),
            self.edits(new="self.assertEqual(result, 25.2)\n        self.skipTest('skip')"),
            '{"edits": [',
        ]
        for response in responses:
            with self.subTest(response=response), self.assertRaises((ValueError, SyntaxError)):
                validated_numeric_edits(self.INITIAL, response, self.FAILURE)
        with self.assertRaises(ValueError):
            validated_numeric_edits(self.INITIAL, self.edits(), "")

    def test_duplicate_text_is_resolved_only_at_a_unique_reported_failure(self):
        original = self.INITIAL + (
            "\n    def test_already_passing(self):\n"
            "        result = 13.2\n"
            "        self.assertEqual(result, 13.2)\n"
        )
        candidate, repairs, _ = validated_numeric_edits(original, self.edits(), self.FAILURE)
        self.assertEqual(candidate, original.replace(
            "self.assertEqual(result, 13.2)", "self.assertEqual(result, 25.2)", 1
        ))
        self.assertEqual([repair["line"] for repair in repairs], [5])
        for failures in ("", self.FAILURE + 'File "/saved/tests.py", line 9, in test_already_passing\n'):
            with self.subTest(failures=failures), self.assertRaisesRegex(ValueError, "unambiguous"):
                validated_numeric_edits(original, self.edits(), failures)

    def test_reference_validation_accepts_only_passing_candidates_without_mutants(self):
        for expected, accepted in ((25.2, True), (24.0, False)):
            with self.subTest(expected=expected), TemporaryDirectory() as directory:
                root = Path(directory)
                shutil.copy2(Path(__file__).parents[1] / "order_calculator.py", root)
                (root / "tests.py").write_text(self.INITIAL)
                runner = ExperimentRunner(efficient_analysis=True)
                data = {
                    "test_file": str(root / "tests.py"), "model": "fixture",
                    "strategy": "simple_prompting", "context_type": "full_context",
                    "timestamp": "fixture", "response_time": 0
                }
                analysis = {
                    "compilation": {
                        "compilation_success": True, "execution_success": False,
                        "tests_run": 1, "test_errors": [self.FAILURE]
                    }
                }
                with patch.object(runner, "run_mutation_testing") as mutation:
                    refined = refine_failed_suite(
                        runner, root, data, analysis,
                        response=self.edits(new=f"self.assertEqual(result, {expected})")
                    )
                self.assertEqual(refined["audit"]["accepted"], accepted)
                self.assertEqual((root / "tests.py").read_text(), self.INITIAL)
                mutation.assert_not_called()
                self.assertTrue((root / "refinement_001/repair_audit.json").exists())

    def test_model_failure_is_audited_without_retry_or_original_changes(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy2(Path(__file__).parents[1] / "order_calculator.py", root)
            (root / "tests.py").write_text(self.INITIAL)
            analysis = {
                "compilation": {
                    "compilation_success": True, "execution_success": False,
                    "tests_run": 1, "test_errors": [self.FAILURE]
                }
            }
            with patch("automation.cli_automation.qwen_client.QwenClient.send_prompt",
                       side_effect=RuntimeError("Incomplete generation")) as request:
                from automation.cli_automation.qwen_client import QwenClient
                with QwenClient(api_key="fixture-secret") as client:
                    result = refine_failed_suite(
                        ExperimentRunner(efficient_analysis=True), root, {}, analysis, client=client
                    )
            self.assertFalse(result["audit"]["accepted"])
            self.assertIsNone(result["analysis"])
            self.assertEqual(request.call_count, 1)
            self.assertEqual((root / "tests.py").read_text(), self.INITIAL)
            self.assertTrue((root / "refinement_001/repair_audit.json").exists())


if __name__ == "__main__":
    unittest.main()
