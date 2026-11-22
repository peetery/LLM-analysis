import json
import os
import re
import ssl
import time
from http.client import IncompleteRead
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .base_cli_client import BaseCLIClient

GEMINI_MODEL = "gemini-3.6-flash"


class GeminiAPIClient(BaseCLIClient):
    MODEL = GEMINI_MODEL

    def __init__(self, api_key=None, timeout=300, max_tokens=8192):
        super().__init__(command="google-gemini-api", model=self.MODEL, timeout=timeout)
        self.api_key = (
            api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")
        ).strip()
        self.max_tokens = max_tokens
        self.provider_calls = []
        if not self.check_authentication():
            raise RuntimeError("Enter a Google AI Studio API key or set GEMINI_API_KEY.")

    def check_installation(self):
        return True

    def check_authentication(self):
        return bool(self.api_key)

    def _request(self, method, suffix="", payload=None, list_models=False, on_chunk=None):
        request = Request(
            "https://generativelanguage.googleapis.com/v1beta/models"
            + ("?pageSize=1" if list_models else "/" + self.model + suffix),
            data=json.dumps(payload).encode() if payload is not None else None,
            headers={
                "x-goog-api-key": self.api_key,
                "Content-Type": "application/json",
                "Accept": "text/event-stream"
                if suffix.endswith("?alt=sse")
                else "application/json",
            },
            method=method,
        )
        started = time.monotonic()
        try:
            with urlopen(request, timeout=self.timeout) as response:
                if suffix.endswith("?alt=sse"):
                    return self._read_stream(response, started, on_chunk)
                return json.load(response)
        except HTTPError as exc:
            raise RuntimeError(
                f"Google Gemini request failed (HTTP {exc.code}); not retried."
            ) from None
        except (URLError, TimeoutError, ConnectionError, IncompleteRead, ssl.SSLError) as exc:
            reason = getattr(exc, "reason", exc)
            if isinstance(reason, TimeoutError):
                message = (
                    f"Google Gemini timed out waiting for response data ({self.timeout}s); "
                    "no automatic retry. Check your network/proxy or try again later."
                )
            elif isinstance(reason, ssl.SSLCertVerificationError):
                message = "Google Gemini TLS certificate verification failed; not retried."
            elif isinstance(reason, (IncompleteRead, ConnectionError, ssl.SSLEOFError)):
                message = "Google Gemini connection closed before completion; not retried."
            else:
                message = "Google Gemini connection failed; check your network/proxy. Not retried."
            raise RuntimeError(message) from None
        finally:
            self.last_response_time = time.monotonic() - started

    def _read_stream(self, response, started, on_chunk):
        result, parts, data = {}, [], []
        characters = 0
        for raw_line in response:
            if time.monotonic() - started > 600:
                raise RuntimeError("Google Gemini generation exceeded 600s; not retried.")
            line = raw_line.decode("utf-8").rstrip("\r\n")
            if line.startswith("data:"):
                data.append(line[5:].lstrip(" "))
            elif not line and data:
                event = json.loads("\n".join(data))
                data.clear()
                if not isinstance(event, dict):
                    raise RuntimeError("Google returned invalid stream data.")
                if "error" in event:
                    code = event["error"].get("code")
                    status = f"HTTP {code}" if type(code) is int else "API error"
                    raise RuntimeError(f"Google Gemini stream failed ({status}); not retried.")
                version = event.get("modelVersion")
                if version:
                    if not re.fullmatch(re.escape(self.model) + r"(?:-\d+(?:-\d+)*)?", version):
                        raise RuntimeError("Google returned an unexpected model identity.")
                    result["modelVersion"] = version
                if "usageMetadata" in event:
                    result["usageMetadata"] = event["usageMetadata"]
                candidates = event.get("candidates", [])
                if len(candidates) > 1:
                    raise RuntimeError("Google returned multiple streamed completions.")
                if candidates:
                    candidate = candidates[0]
                    if candidate.get("index", 0) != 0:
                        raise RuntimeError("Google returned an unexpected completion index.")
                    for part in candidate.get("content", {}).get("parts", []):
                        if not part.get("thought"):
                            parts.append(part)
                            characters += len(part.get("text", ""))
                    if on_chunk is not None:
                        on_chunk(characters)
                    if candidate.get("finishReason"):
                        result["candidates"] = [
                            {
                                "finishReason": candidate["finishReason"],
                                "content": {"parts": parts},
                            }
                        ]
                        return result
        raise RuntimeError("Gemini stream ended without a completed response; not evaluated.")

    def check_api_key(self):
        result = self._request("GET", list_models=True)
        models = result.get("models", [])
        if not isinstance(models, list):
            raise RuntimeError("Google returned an invalid model-list response.")
        return {"provider": "google", "authenticated": True, "models_returned": len(models)}

    def send_prompt(self, prompt, **kwargs):
        config = {
            "temperature": 0.2,
            "maxOutputTokens": self.max_tokens,
            "thinkingConfig": {"thinkingLevel": "LOW"},
        }
        if kwargs.get("response_mime_type") == "application/json":
            config["responseMimeType"] = "application/json"
        result = self._request(
            "POST",
            ":streamGenerateContent?alt=sse",
            {
                "model": "models/" + self.model,
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": config,
            },
            on_chunk=kwargs.get("on_chunk"),
        )
        version = result.get("modelVersion", "")
        if not re.fullmatch(re.escape(self.model) + r"(?:-\d+(?:-\d+)*)?", version):
            raise RuntimeError("Google returned an unexpected or missing model identity.")
        candidates = result.get("candidates", [])
        if len(candidates) != 1:
            raise RuntimeError("Google returned no single text completion.")
        candidate = candidates[0]
        reason = candidate.get("finishReason")
        normalized = (
            "stop" if reason == "STOP" else "length" if reason == "MAX_TOKENS" else str(reason)
        )
        self.provider_calls.append(
            {
                "provider": "google",
                "model": self.model,
                "model_version": version,
                "finish_reason": normalized,
                "native_finish_reason": reason,
                "usage": result.get("usageMetadata", {}),
                "seconds": self.last_response_time,
                "max_tokens": self.max_tokens,
                "temperature": 0.2,
                "thinking_level": "low",
                "transport": "streaming_sse",
                "timeout_seconds": self.timeout,
            }
        )
        if reason != "STOP":
            raise RuntimeError("Gemini output was incomplete or blocked; not evaluated.")
        parts = candidate.get("content", {}).get("parts", [])
        if any("functionCall" in part for part in parts):
            raise RuntimeError("Gemini returned an unsupported tool call.")
        content = "".join(
            part["text"]
            for part in parts
            if isinstance(part.get("text"), str) and not part.get("thought")
        )
        if not content.strip():
            raise RuntimeError("Gemini returned no test text.")
        return content

    def cleanup(self):
        self.api_key = ""
