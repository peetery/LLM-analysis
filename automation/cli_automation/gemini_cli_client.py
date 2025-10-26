"""
Gemini CLI Client

This client uses Gemini CLI's `-p` (prompt) flag for non-interactive automation.

Authentication:
    Option 1 (Recommended): Login via Google Account (automatic)
    Option 2: Use API key via GEMINI_API_KEY environment variable

Models available:
    - gemini-2.5-pro: Gemini 2.5 Pro (most capable, GA)
    - gemini-2.5-flash: Gemini 2.5 Flash (fast, GA)
"""

import subprocess
import tempfile
import logging
import platform
import time
import json
import os
from pathlib import Path

from .base_cli_client import BaseCLIClient

logger = logging.getLogger(__name__)


class GeminiCLIClient(BaseCLIClient):

    SUPPORTED_MODELS = [
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
    ]

    MODEL_ALIASES = {
        "gemini-2.5-pro": "gemini-2.5-pro",
        "gemini-2.5-flash": "gemini-2.5-flash",
        "gemini-2.0-flash": "gemini-2.0-flash",
    }

    def __init__(self, model: str = "gemini-2.5-flash", timeout: int = 300):
        actual_model = self.MODEL_ALIASES.get(model, model)

        if actual_model not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Unsupported model: {model}. "
                f"Supported models: {', '.join(self.SUPPORTED_MODELS)}"
            )

        model = actual_model

        command = "gemini.cmd" if platform.system() == "Windows" else "gemini"

        super().__init__(command=command, model=model, timeout=timeout)

        if not self.check_installation():
            raise RuntimeError(
                "Gemini CLI is not installed or not in PATH. "
                "Install with: npm install -g @google/gemini-cli"
            )

        if not self.check_authentication():
            logger.warning(
                "Could not verify Gemini authentication. "
                "Make sure you're logged in (run: gemini login) or set GEMINI_API_KEY"
            )

        logger.info(f"Gemini CLI client initialized with model: {model}")

    def check_installation(self) -> bool:
        try:
            result = subprocess.run(
                [self.command, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
                shell=False
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                logger.info(f"Gemini CLI is installed: {version}")
                return True
            else:
                logger.error(f"Gemini CLI returned error code {result.returncode}")
                return False

        except FileNotFoundError:
            logger.error("Gemini CLI not found in PATH")
            logger.error("Install with: npm install -g @google/gemini-cli")
            return False
        except subprocess.TimeoutExpired:
            logger.error("Gemini CLI version check timed out")
            return False
        except Exception as e:
            logger.error(f"Error checking installation: {e}")
            return False

    def check_authentication(self) -> bool:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            logger.info("✓ GEMINI_API_KEY found")
            return True

        logger.info("✓ Skipping auth check (assuming logged in via 'gemini login')")
        logger.info("   If not logged in, run: gemini login")
        return True

    def send_prompt(self, prompt: str, **kwargs) -> str:
        """
        Send prompt to Gemini CLI using -p flag

        Uses `-p --output-format json --allowed-tools ""` for reliable non-interactive output.
        The --allowed-tools "" flag is CRITICAL - it prevents Gemini from using Write/Edit/Bash
        tools and forces it to return code in the response field.

        Args:
            prompt: The prompt text
            **kwargs: Additional arguments
                - is_final_step: bool - if True, adds instruction to return code (for CoT)
        """
        logger.info(f"Sending prompt to Gemini CLI ({len(prompt)} chars)")

        is_final_step = kwargs.get('is_final_step', True)

        if is_final_step:
            enhanced_prompt = f"""{prompt}

IMPORTANT: Return the complete code in your response. Do NOT use write_file, edit_file, or any other tools. Just provide the code directly in your answer."""
        else:
            enhanced_prompt = prompt
            logger.debug("Skipping 'return code' instruction (not final step)")

        start_time = time.time()

        # Write prompt to temp file (more reliable than stdin on Windows)
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.txt',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(enhanced_prompt)
            prompt_file = f.name

        try:
            cmd_parts = [self.command, '-p', '--output-format', 'json', '--allowed-tools', '""']

            if self.model:
                cmd_parts.extend(['-m', self.model])

            cmd_str = ' '.join(cmd_parts) + f' < "{prompt_file}"'

            result = subprocess.run(
                cmd_str,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                shell=True
            )

            elapsed_time = time.time() - start_time
            self.last_response_time = elapsed_time
            logger.info(f"Gemini CLI response received in {elapsed_time:.2f}s")

            if result.returncode != 0:
                logger.error(f"Command failed with return code {result.returncode}")
                logger.error(f"stderr: {result.stderr}")
                logger.error(f"stdout: {result.stdout[:500]}")
                raise RuntimeError(
                    f"Gemini command failed. stderr: {result.stderr}, "
                    f"stdout: {result.stdout[:200]}"
                )

            try:
                response_data = json.loads(result.stdout)

                result_text = None

                if isinstance(response_data, dict):
                    if "response" in response_data:
                        result_text = response_data.get("response", "")
                    elif "result" in response_data:
                        result_text = response_data.get("result", "")
                    elif "text" in response_data:
                        result_text = response_data.get("text", "")
                    elif "output" in response_data:
                        result_text = response_data.get("output", "")

                if result_text:
                    logger.info(f"Received Gemini response ({len(result_text)} chars)")

                    if '```python' in result_text:
                        logger.info("✓ Response contains ```python code blocks")
                    elif '```' in result_text:
                        logger.info("✓ Response contains generic ``` code blocks")
                    elif 'import unittest' in result_text or 'def test' in result_text:
                        logger.info("✓ Response appears to be raw Python code")
                    else:
                        logger.warning("⚠️ Response doesn't appear to contain code")

                    return result_text

                logger.error(f"Could not extract result from JSON response")
                logger.error(f"Response keys: {list(response_data.keys()) if isinstance(response_data, dict) else 'not a dict'}")
                logger.error(f"Response structure: {json.dumps(response_data, indent=2)[:1000]}")
                raise RuntimeError("No code generated in Gemini response")

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Raw output: {result.stdout[:500]}")

                if 'import unittest' in result.stdout or 'def test' in result.stdout:
                    logger.info("Fallback: treating raw output as code")
                    return result.stdout

                raise RuntimeError(f"Invalid JSON response from Gemini: {e}")

        finally:
            Path(prompt_file).unlink(missing_ok=True)

    def set_model(self, model: str):
        if model not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Unsupported model: {model}. "
                f"Supported models: {', '.join(self.SUPPORTED_MODELS)}"
            )

        self.model = model
        logger.info(f"Switched to model: {model}")

    def get_available_models(self) -> list:
        return self.SUPPORTED_MODELS.copy()

    def send_prompt_with_context(self, prompt: str, context_files: list = None) -> str:
        if not context_files:
            return self.send_prompt(prompt)

        logger.info(f"Sending prompt with {len(context_files)} context files")

        logger.warning("Context files not yet implemented for Gemini CLI")
        return self.send_prompt(prompt)
