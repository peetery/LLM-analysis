import io
import json
import threading
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from qwen_ui import REPORT_MARKER, RequestError, Runs, make_server, run_worker
from automation.cli_automation.gemini_api_client import GeminiAPIClient


class TestQwenUI(unittest.TestCase):
    SOURCE = "def double(value):\n    return value * 2\n"

    def test_invalid_sources_and_duplicate_runs_never_start_paid_work(self):
        with TemporaryDirectory() as directory:
            runs = Runs(directory)
            valid = {
                "filename": "example.py",
                "source": self.SOURCE,
                "api_key": "fixture-key",
                "fresh": True,
                "budget": 2,
            }
            with patch("qwen_ui.threading.Thread") as thread:
                for change in (
                    {"filename": "../example.py"},
                    {"filename": "tests.py"},
                    {"source": "def broken("},
                    {"api_key": ""},
                    {"budget": True},
                    {"fresh": "true"},
                ):
                    with self.subTest(change=change), self.assertRaises(RequestError):
                        runs.start({**valid, **change})
                thread.assert_not_called()
                job_id = runs.start(valid)
                with self.assertRaisesRegex(RequestError, "already active"):
                    runs.start(valid)
                self.assertNotIn("fixture-key", json.dumps(runs.get(job_id)))
                self.assertEqual(
                    (
                        Path(directory) / "qwen_results/ui_sources" / job_id / "example.py"
                    ).read_text(),
                    self.SOURCE,
                )

    def test_http_progress_artifacts_and_key_isolation(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "order_calculator.py").write_text(self.SOURCE)
            result = root / "qwen_results/verified/fixture"
            result.mkdir(parents=True)
            (result / "tests.py").write_text("generated test fixture\n")
            report = {
                "quality_passed": True,
                "status": "verified",
                "cache_hit": False,
                "model_requests_this_run": 1,
                "result_dir": str(result),
                "mutation_score": 91,
                "baseline": {"status": "passed", "tests": 2, "branch_coverage": 98},
            }
            (result / "report.json").write_text(json.dumps(report))
            process = Mock()
            process.stdin = io.StringIO()
            process.stdout = io.StringIO(
                "Progress fixture-key must be redacted\n"
                + REPORT_MARKER
                + json.dumps(report)
                + "\n"
            )
            process.poll.return_value = 0
            runs = Runs(root)
            server = make_server(runs, 0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            base = "http://127.0.0.1:" + str(server.server_port)

            def request(path, data=None, token=True):
                headers = {"X-Qwen-UI-Token": runs.token} if token else {}
                body = json.dumps(data).encode() if data is not None else None
                with urlopen(
                    Request(base + path, data=body, headers=headers), timeout=3
                ) as response:
                    return response.read()

            try:
                self.assertIn(b"Fresh paid LLM generation", request("/"))
                with self.assertRaises(HTTPError) as denied:
                    request("/api/samples", token=False)
                self.assertEqual(denied.exception.code, 403)
                self.assertEqual(json.loads(request("/api/samples"))[0]["source"], self.SOURCE)
                with patch("qwen_ui.subprocess.Popen", return_value=process) as launch:
                    started = json.loads(
                        request(
                            "/api/runs",
                            {
                                "filename": "example.py",
                                "source": self.SOURCE,
                                "api_key": "fixture-key",
                                "fresh": True,
                                "budget": 1,
                            },
                        )
                    )
                    deadline = time.monotonic() + 3
                    while True:
                        job = json.loads(request("/api/runs/" + started["id"]))
                        if job["status"] != "running" or time.monotonic() >= deadline:
                            break
                        time.sleep(0.01)
                    self.assertEqual(job["status"], "verified")
                    self.assertEqual(json.loads(request("/api/current"))["id"], started["id"])
                    self.assertIn("[redacted]", "\n".join(job["logs"]))
                    self.assertNotIn("fixture-key", json.dumps(job))
                    self.assertNotIn("fixture-key", str(launch.call_args))
                    self.assertNotIn("OPENROUTER_API_KEY", launch.call_args.kwargs["env"])
                artifact = "/api/runs/" + started["id"] + "/artifacts/"
                self.assertEqual(request(artifact + "tests.py"), b"generated test fixture\n")
                with self.assertRaises(HTTPError):
                    request(artifact + "source.py")
                report["result_dir"] = str(root)
                with runs.lock:
                    runs.jobs[started["id"]]["report"] = report
                with self.assertRaises(HTTPError):
                    request(artifact + "tests.py")
            finally:
                server.shutdown()
                server.server_close()
                runs.stop()
                thread.join(timeout=3)

    def test_worker_uses_verified_backend_and_does_not_echo_key(self):
        payload = {
            "source_file": "/unused/example.py",
            "root": "/unused",
            "api_key": "fixture-key",
            "fresh": True,
            "budget": 1,
        }
        output = io.StringIO()

        def backend(source, results, cache, factory, **kwargs):
            self.assertEqual(
                kwargs,
                {
                    "mutation_target": 60.0,
                    "branch_target": 98.0,
                    "max_refinements": 1,
                    "fresh": True,
                    "model": GeminiAPIClient.MODEL,
                },
            )
            client = factory()
            self.assertIsInstance(client, GeminiAPIClient)
            self.assertEqual(client.api_key, "fixture-key")
            response = {
                "modelVersion": GeminiAPIClient.MODEL,
                "candidates": [
                    {"finishReason": "STOP", "content": {"parts": [{"text": "pass\n"}]}}
                ],
            }
            with patch(
                "automation.cli_automation.gemini_api_client.urlopen",
                return_value=io.BytesIO(("data: " + json.dumps(response) + "\n\n").encode()),
            ):
                self.assertEqual(client.send_prompt("fixture"), "pass\n")
            client.cleanup()
            return {
                "status": "blocked",
                "quality_passed": False,
                "error": "fixture-key",
                "model_requests_this_run": 1,
            }

        with (
            patch("qwen_ui.sys.stdin", io.StringIO(json.dumps(payload))),
            patch("automation.verified_qwen.run_verified", side_effect=backend),
            redirect_stdout(output),
        ):
            run_worker()
        self.assertNotIn("fixture-key", output.getvalue())
        self.assertIn("Gemini stream active: 5 test characters received", output.getvalue())
        report = json.loads(output.getvalue().split(REPORT_MARKER, 1)[1])
        self.assertFalse(report["quality_passed"])
        self.assertEqual(report["error"], "[redacted]")


if __name__ == "__main__":
    unittest.main()
