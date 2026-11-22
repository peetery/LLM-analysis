import io
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.error import HTTPError

from automation.cli_automation.qwen_client import QwenClient


class TestQwenClient(unittest.TestCase):
    def completion(self, finish_reason="stop", model=QwenClient.MODEL):
        return {
            "model": model,
            "choices": [{"finish_reason": finish_reason, "message": {"content": "import unittest"}}],
            "usage": {"prompt_tokens": 100, "completion_tokens": 10}
        }

    def test_transport_returns_generated_code_and_records_usage_without_key(self):
        with patch(
            "automation.cli_automation.qwen_client.urlopen",
            return_value=io.BytesIO(json.dumps(self.completion()).encode())
        ) as transport:
            with QwenClient(api_key="fixture-secret") as client:
                self.assertEqual(client.send_prompt("Generate tests"), "import unittest")
                request = transport.call_args.args[0]
                payload = json.loads(request.data)
                self.assertEqual(payload["model"], QwenClient.MODEL)
                self.assertEqual(payload["messages"], [{"role": "user", "content": "Generate tests"}])
                self.assertEqual(request.get_header("Authorization"), "Bearer fixture-secret")
                self.assertEqual(client.provider_calls[0]["usage"]["completion_tokens"], 10)
                self.assertNotIn("fixture-secret", json.dumps(client.provider_calls))
                self.assertNotIn("fixture-secret", repr(client))
            self.assertEqual(client.api_key, "")

    def test_truncation_and_model_substitution_are_rejected(self):
        for result in (self.completion("length"), self.completion(model="other")):
            with self.subTest(result=result), patch(
                "automation.cli_automation.qwen_client.urlopen",
                return_value=io.BytesIO(json.dumps(result).encode())
            ):
                with QwenClient(api_key="fixture-secret") as client:
                    with self.assertRaises(RuntimeError):
                        client.send_prompt("Generate tests")

    def test_authentication_errors_are_not_retried_or_logged_with_credentials(self):
        with patch(
            "automation.cli_automation.qwen_client.urlopen",
            side_effect=HTTPError("https://openrouter.ai", 401, "fixture-secret", {}, None)
        ) as transport:
            with QwenClient(api_key="fixture-secret") as client:
                with self.assertRaisesRegex(RuntimeError, "HTTP 401") as caught:
                    client.send_prompt("Generate tests")
                self.assertNotIn("fixture-secret", str(caught.exception))
                self.assertEqual(transport.call_count, 1)

    def test_cli_reports_failed_generated_tests_without_claiming_success(self):
        root = Path(__file__).parents[1]
        with TemporaryDirectory() as directory:
            script = (
                "import runpy, sys\n"
                "from unittest.mock import patch\n"
                f"sys.path.insert(0, {str(root / 'automation')!r})\n"
                f"sys.argv = ['cli_experiment_runner.py', '--model', 'qwen3-coder-30b', "
                f"'--source-file', {str(root / 'order_calculator.py')!r}, "
                "'--class-name', 'OrderCalculator', '--strategy', 'simple_prompting', "
                "'--context', 'full_context', '--efficient-analysis', "
                f"'--results-dir', {directory!r}]\n"
                "code = 'import unittest\\nclass Tests(unittest.TestCase):\\n"
                "    def test_wrong(self):\\n        self.assertEqual(1, 2)\\n'\n"
                "with patch('cli_automation.qwen_client.QwenClient.send_prompt', "
                "return_value=code):\n"
                f"    runpy.run_path({str(root / 'automation/cli_experiment_runner.py')!r}, "
                "run_name='__main__')\n"
            )
            result = subprocess.run(
                [sys.executable, '-c', script], cwd=directory,
                env={**os.environ, 'OPENROUTER_API_KEY': 'fixture-secret'},
                text=True, capture_output=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('1/1 tests failed', result.stdout)
            self.assertNotIn('completed successfully', result.stdout + result.stderr)
            self.assertNotIn('fixture-secret', result.stdout + result.stderr)
            report = json.loads(next(Path(directory).rglob('analysis_results.json')).read_text())
            self.assertFalse(report['compilation']['execution_success'])
            self.assertIsNone(report['mutation'])

    def test_cli_opt_in_makes_one_repair_call_and_preserves_original_run(self):
        root = Path(__file__).parents[1]
        code = (
            "import unittest\nclass Tests(unittest.TestCase):\n"
            "    def test_total(self):\n"
            "        result = 25.2\n"
            "        self.assertEqual(result, 13.2)\n"
        )
        edits = json.dumps({"edits": [{
            "old": "self.assertEqual(result, 13.2)",
            "new": "self.assertEqual(result, 25.2)",
            "reason": "(11 + 10) * 1.2 = 25.2"
        }]})
        with TemporaryDirectory() as directory:
            script = (
                "import runpy, sys\nfrom unittest.mock import patch\n"
                f"sys.path.insert(0, {str(root / 'automation')!r})\n"
                f"sys.argv = ['cli_experiment_runner.py', '--model', 'qwen3-coder-30b', "
                f"'--source-file', {str(root / 'order_calculator.py')!r}, "
                "'--class-name', 'OrderCalculator', '--strategy', 'simple_prompting', "
                "'--context', 'full_context', '--efficient-analysis', '--refine-failures', "
                f"'--results-dir', {directory!r}]\n"
                "with patch('cli_automation.qwen_client.QwenClient.send_prompt', "
                f"side_effect={[code, edits]!r}) as model:\n"
                f"    runpy.run_path({str(root / 'automation/cli_experiment_runner.py')!r}, "
                "run_name='__main__')\n"
                "    assert model.call_count == 2\n"
            )
            result = subprocess.run(
                [sys.executable, '-c', script], cwd=directory,
                env={**os.environ, 'OPENROUTER_API_KEY': 'fixture-secret'},
                text=True, capture_output=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Refinement accepted: True", result.stdout)
            original = next(Path(directory).rglob("experiment_results.json")).parent
            initial = json.loads((original / "analysis_results.json").read_text())
            refined = json.loads((original / "refinement_001/analysis_results.json").read_text())
            self.assertFalse(initial["compilation"]["execution_success"])
            self.assertTrue(refined["compilation"]["execution_success"])
            self.assertEqual((original / "tests.py").read_text().count("result, 13.2"), 1)
            self.assertIsNone(refined["mutation"])


if __name__ == "__main__":
    unittest.main()
