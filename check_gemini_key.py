import argparse
import getpass
import io
import json
import sys
from unittest.mock import patch

from automation.cli_automation.gemini_api_client import GeminiAPIClient


def main():
    parser = argparse.ArgumentParser(
        description="Check Google API authentication without generating text."
    )
    parser.add_argument(
        "--mock", action="store_true", help="Use a dummy key and mock response; no network."
    )
    args = parser.parse_args()
    if args.mock:
        with (
            patch(
                "automation.cli_automation.gemini_api_client.urlopen",
                return_value=io.BytesIO(b'{"models": [{"name": "models/mock-model"}]}'),
            ),
            GeminiAPIClient(api_key="mock-only-not-a-real-key") as client,
        ):
            result = client.check_api_key()
        print(
            json.dumps(
                {**result, "mock": True, "real_key_tested": False, "generation_requests": 0},
                indent=2,
            )
        )
        return 0
    if not sys.stdin.isatty():
        print(
            "Run in an interactive Terminal; keys are accepted only through a hidden prompt.",
            file=sys.stderr,
        )
        return 2
    key = getpass.getpass("Google Gemini API key (hidden): ").strip()
    if not key:
        print("No key entered; no request made.", file=sys.stderr)
        return 2
    try:
        with GeminiAPIClient(api_key=key) as client:
            result = client.check_api_key()
        print(json.dumps({**result, "mock": False, "generation_requests": 0}, indent=2))
        return 0
    except RuntimeError as exc:
        print(json.dumps({"authenticated": False, "error": str(exc)}, indent=2))
        return 2
    finally:
        key = ""


if __name__ == "__main__":
    raise SystemExit(main())
