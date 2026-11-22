import json
import os
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .base_cli_client import BaseCLIClient


class QwenClient(BaseCLIClient):
    MODEL = "qwen/qwen3-coder-30b-a3b-instruct"

    def __init__(self, api_key=None, timeout=180, max_tokens=6000):
        super().__init__(command="openrouter", model=self.MODEL, timeout=timeout)
        self.api_key = (api_key or os.environ.get("OPENROUTER_API_KEY", "")).strip()
        self.max_tokens = max_tokens
        self.provider_calls = []
        if not self.check_authentication():
            raise RuntimeError("Set OPENROUTER_API_KEY or use --prompt-key.")

    def check_installation(self):
        return True

    def check_authentication(self):
        return bool(self.api_key)

    def send_prompt(self, prompt, **kwargs):
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": self.max_tokens,
            "provider": {"allow_fallbacks": False}
        }
        request = Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": "Bearer " + self.api_key,
                "Content-Type": "application/json"
            },
            method="POST"
        )
        started = time.monotonic()
        try:
            with urlopen(request, timeout=self.timeout) as response:
                result = json.load(response)
        except HTTPError as exc:
            raise RuntimeError(f"OpenRouter request failed (HTTP {exc.code}); not retried.") from None
        except (URLError, TimeoutError):
            raise RuntimeError("OpenRouter connection failed; not retried.") from None
        finally:
            self.last_response_time = time.monotonic() - started
        if result.get("model") != self.model:
            raise RuntimeError("OpenRouter returned an unexpected model.")
        choices = result.get("choices", [])
        if not choices:
            raise RuntimeError("OpenRouter returned no completion.")
        choice = choices[0]
        self.provider_calls.append({
            "model": result["model"],
            "finish_reason": choice.get("finish_reason"),
            "usage": result.get("usage", {}),
            "seconds": self.last_response_time,
            "max_tokens": self.max_tokens,
            "temperature": 0.2
        })
        if choice.get("finish_reason") != "stop":
            raise RuntimeError("Qwen output was truncated or incomplete; not evaluated.")
        content = choice.get("message", {}).get("content")
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("Qwen returned no test text.")
        return content

    def cleanup(self):
        self.api_key = ""
