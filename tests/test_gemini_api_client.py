import io
import json
import unittest
from http.client import IncompleteRead
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from automation.cli_automation.gemini_api_client import GEMINI_MODEL, GeminiAPIClient


def stream_response(*events):
    return io.BytesIO("".join("data: " + json.dumps(event) + "\n\n" for event in events).encode())


class TestGeminiAPIClient(unittest.TestCase):
    def test_mock_key_check_uses_google_header_not_url_and_makes_no_generation(self):
        response = {"models": [{"name": "models/" + GEMINI_MODEL}]}
        with (
            patch(
                "automation.cli_automation.gemini_api_client.urlopen",
                return_value=io.BytesIO(json.dumps(response).encode()),
            ) as transport,
            GeminiAPIClient(api_key="fixture-google-key") as client,
        ):
            result = client.check_api_key()
            request = transport.call_args.args[0]
            self.assertTrue(result["authenticated"])
            self.assertEqual(request.get_method(), "GET")
            self.assertEqual(request.get_header("X-goog-api-key"), "fixture-google-key")
            self.assertNotIn("fixture-google-key", request.full_url)
            self.assertTrue(request.full_url.endswith("/models?pageSize=1"))
            self.assertIsNone(request.data)
            self.assertEqual(client.provider_calls, [])
            self.assertEqual(transport.call_count, 1)
        self.assertEqual(client.api_key, "")

    def test_mock_invalid_key_errors_do_not_echo_credentials_or_retry(self):
        for status in (400, 401, 403, 429):
            with (
                self.subTest(status=status),
                patch(
                    "automation.cli_automation.gemini_api_client.urlopen",
                    side_effect=HTTPError(
                        "https://generativelanguage.googleapis.com",
                        status,
                        "fixture-google-key",
                        {},
                        None,
                    ),
                ) as transport,
                GeminiAPIClient(api_key="fixture-google-key") as client,
            ):
                with self.assertRaisesRegex(RuntimeError, "HTTP " + str(status)) as caught:
                    client.check_api_key()
                self.assertNotIn("fixture-google-key", str(caught.exception))
                self.assertEqual(transport.call_count, 1)

    def test_mock_generation_records_native_identity_and_omits_thoughts(self):
        response = {
            "modelVersion": GEMINI_MODEL,
            "candidates": [
                {
                    "finishReason": "STOP",
                    "content": {
                        "parts": [
                            {"text": "private reasoning", "thought": True},
                            {"text": "import unittest\n"},
                        ]
                    },
                }
            ],
            "usageMetadata": {"promptTokenCount": 2, "candidatesTokenCount": 3},
        }
        with (
            patch(
                "automation.cli_automation.gemini_api_client.urlopen",
                return_value=stream_response(response),
            ) as transport,
            GeminiAPIClient(api_key="fixture-google-key") as client,
        ):
            self.assertEqual(
                client.send_prompt("fixture prompt", response_mime_type="application/json"),
                "import unittest\n",
            )
            request = transport.call_args.args[0]
            payload = json.loads(request.data)
            self.assertTrue(request.full_url.endswith(":streamGenerateContent?alt=sse"))
            self.assertEqual(payload["generationConfig"]["responseMimeType"], "application/json")
            self.assertEqual(client.provider_calls[0]["finish_reason"], "stop")
            self.assertEqual(client.provider_calls[0]["provider"], "google")
            self.assertNotIn("fixture-google-key", json.dumps(client.provider_calls))

    def test_mock_truncated_generation_and_wrong_model_are_rejected(self):
        for change in ({"finishReason": "MAX_TOKENS"}, {"modelVersion": "other-model"}):
            response = {
                "modelVersion": change.get("modelVersion", GEMINI_MODEL),
                "candidates": [
                    {
                        "finishReason": change.get("finishReason", "STOP"),
                        "content": {"parts": [{"text": "partial"}]},
                    }
                ],
            }
            with (
                self.subTest(change=change),
                patch(
                    "automation.cli_automation.gemini_api_client.urlopen",
                    return_value=stream_response(response),
                ),
                GeminiAPIClient(api_key="fixture-google-key") as client,
                self.assertRaises(RuntimeError),
            ):
                client.send_prompt("fixture prompt")

    def test_stream_assembles_chunks_and_reports_progress_without_thoughts(self):
        events = [
            {
                "modelVersion": GEMINI_MODEL,
                "candidates": [
                    {"content": {"parts": [{"text": "private thought", "thought": True}]}}
                ],
            },
            {"candidates": [{"content": {"parts": [{"text": "import "}]}}]},
            {
                "candidates": [
                    {"finishReason": "STOP", "content": {"parts": [{"text": "unittest\n"}]}}
                ],
                "usageMetadata": {"candidatesTokenCount": 3},
            },
        ]
        progress = []
        with (
            patch(
                "automation.cli_automation.gemini_api_client.urlopen",
                return_value=stream_response(*events),
            ) as transport,
            GeminiAPIClient(api_key="fixture-google-key") as client,
        ):
            self.assertEqual(
                client.send_prompt("fixture", on_chunk=progress.append), "import unittest\n"
            )
            self.assertEqual(progress, [0, 7, 16])
            self.assertEqual(client.provider_calls[0]["usage"]["candidatesTokenCount"], 3)
            self.assertEqual(transport.call_count, 1)

    def test_stream_disconnect_and_api_errors_never_admit_partial_text(self):
        for events in (
            [
                {
                    "modelVersion": GEMINI_MODEL,
                    "candidates": [{"content": {"parts": [{"text": "partial"}]}}],
                }
            ],
            [{"error": {"code": 429, "message": "fixture-google-key"}}],
        ):
            with (
                self.subTest(events=events),
                patch(
                    "automation.cli_automation.gemini_api_client.urlopen",
                    return_value=stream_response(*events),
                ) as transport,
                GeminiAPIClient(api_key="fixture-google-key") as client,
            ):
                with self.assertRaises(RuntimeError) as caught:
                    client.send_prompt("fixture")
                self.assertNotIn("fixture-google-key", str(caught.exception))
                self.assertEqual(client.provider_calls, [])
                self.assertEqual(transport.call_count, 1)

    def test_connection_timeout_is_explicit_without_key_echo_or_retry(self):
        for error in (
            TimeoutError("fixture-google-key"),
            URLError(TimeoutError("fixture-google-key")),
        ):
            with (
                self.subTest(error=type(error).__name__),
                patch(
                    "automation.cli_automation.gemini_api_client.urlopen", side_effect=error
                ) as transport,
                GeminiAPIClient(api_key="fixture-google-key", timeout=17) as client,
            ):
                with self.assertRaisesRegex(RuntimeError, r"timed out.*17s") as caught:
                    client.send_prompt("fixture")
                self.assertNotIn("fixture-google-key", str(caught.exception))
                self.assertEqual(transport.call_count, 1)

    def test_stream_idle_keepalives_cannot_run_past_generation_deadline(self):
        with (
            patch(
                "automation.cli_automation.gemini_api_client.urlopen",
                return_value=io.BytesIO(b": keepalive\n\n"),
            ) as transport,
            patch(
                "automation.cli_automation.gemini_api_client.time.monotonic",
                side_effect=[0, 601, 602],
            ),
            GeminiAPIClient(api_key="fixture-google-key") as client,
        ):
            with self.assertRaisesRegex(RuntimeError, "exceeded 600s"):
                client.send_prompt("fixture")
            self.assertEqual(client.provider_calls, [])
            self.assertEqual(transport.call_count, 1)

    def test_connection_closed_errors_never_echo_response_bytes_or_retry(self):
        with (
            patch(
                "automation.cli_automation.gemini_api_client.urlopen",
                side_effect=IncompleteRead(b"fixture-google-key"),
            ) as transport,
            GeminiAPIClient(api_key="fixture-google-key") as client,
        ):
            with self.assertRaisesRegex(RuntimeError, "connection closed") as caught:
                client.send_prompt("fixture")
            self.assertNotIn("fixture-google-key", str(caught.exception))
            self.assertEqual(transport.call_count, 1)


if __name__ == "__main__":
    unittest.main()
