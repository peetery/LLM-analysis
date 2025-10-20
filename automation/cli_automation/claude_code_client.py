"""
Claude Code CLI Client

This client uses Claude Code's `-p` (print) flag for non-interactive automation.

The `-p` flag provides true non-interactive mode that doesn't cause recursion.

Authentication:
    Automatic via Claude Pro/Team/Enterprise subscription

Models available:
    - claude-sonnet-4.5: Latest Sonnet (recommended)
"""

import subprocess
import tempfile
import logging
import platform
import time
import json
from pathlib import Path

from .base_cli_client import BaseCLIClient

logger = logging.getLogger(__name__)


class ClaudeCodeClient(BaseCLIClient):

    SUPPORTED_MODELS = [
        "claude-sonnet-4-5-20250929",
    ]

    MODEL_ALIASES = {
        "claude-sonnet-4.5": "claude-sonnet-4-5-20250929",
    }

    def __init__(self, model: str = "claude-sonnet-4.5", timeout: int = 300):
        actual_model = self.MODEL_ALIASES.get(model, model)

        if actual_model not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Unsupported model: {model}. "
                f"Supported models: {', '.join(self.MODEL_ALIASES.keys())}"
            )

        model = actual_model

        command = "claude.cmd" if platform.system() == "Windows" else "claude"

        super().__init__(command=command, model=model, timeout=timeout)

        if not self.check_installation():
            raise RuntimeError(
                "Claude CLI is not installed or not in PATH. "
                "Make sure you're running this from within Claude Code."
            )

        if not self.check_authentication():
            logger.warning("Could not verify Claude authentication, proceeding anyway")

        logger.info(f"Claude Code client initialized with model: {model}")

    def check_installation(self) -> bool:
        try:
            result = subprocess.run(
                [self.command, "-p", "test"],
                capture_output=True,
                text=True,
                timeout=30,
                shell=True if platform.system() == "Windows" else False
            )

            if result.returncode == 0:
                logger.info("Claude CLI is installed and working")
                return True
            else:
                logger.error(f"Claude CLI returned error code {result.returncode}")
                logger.error(f"stderr: {result.stderr[:200]}")
                return False

        except FileNotFoundError:
            logger.error("Claude CLI not found in PATH")
            return False
        except subprocess.TimeoutExpired:
            logger.error("Claude CLI test timed out after 30s")
            return False
        except Exception as e:
            logger.error(f"Error checking installation: {e}")
            return False

    def check_authentication(self) -> bool:
        """
        Check if authenticated to Claude

        Claude Code handles authentication automatically.
        This method always returns True as auth is managed by the parent process.
        """
        return True

    def send_prompt(self, prompt: str, **kwargs) -> str:
        """
        Send prompt to Claude Code using -p flag

        Uses `-p --output-format json --max-turns 1` for reliable non-interactive output.
        The --max-turns 1 flag prevents Claude from trying to use tools (Write, Edit, etc.)
        and ensures it returns only text response.

        Note: On Windows, stdin doesn't work reliably with shell=True, so we write
        the prompt to a temporary file.

        Args:
            prompt: The prompt text
            **kwargs: Additional arguments (not used currently)

        Returns:
            Model response text

        Raises:
            RuntimeError: If command fails after retries
        """
        logger.info(f"Sending prompt to Claude Code ({len(prompt)} chars)")

        start_time = time.time()

        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.txt',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(prompt)
            prompt_file = f.name

        try:
            cmd_str = f'{self.command} -p --output-format json'

            if self.model:
                cmd_str += f' --model {self.model}'

            cmd_str += f' < "{prompt_file}"'

            result = subprocess.run(
                cmd_str,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                shell=True
            )

            elapsed_time = time.time() - start_time
            self.last_response_time = elapsed_time
            logger.info(f"Claude Code response received in {elapsed_time:.2f}s")

            if result.returncode != 0:
                logger.error(f"Command failed with return code {result.returncode}")
                logger.error(f"stderr: {result.stderr}")
                logger.error(f"stdout: {result.stdout[:500]}")
                raise RuntimeError(f"Claude command failed. stderr: {result.stderr}, stdout: {result.stdout[:200]}")

            try:
                response_data = json.loads(result.stdout)

                if response_data.get("type") == "result":
                    result_text = response_data.get("result", "")

                    if result_text:
                        logger.info(f"Received Claude response ({len(result_text)} chars)")

                        if '```python' in result_text:
                            logger.info("✓ Response contains ```python code blocks")
                        elif '```' in result_text:
                            logger.info("✓ Response contains generic ``` code blocks")
                        elif 'import unittest' in result_text or 'def test' in result_text:
                            logger.info("✓ Response appears to be raw Python code")
                        else:
                            logger.warning("⚠️ Response doesn't appear to contain code")

                        return result_text

                    permission_denials = response_data.get("permission_denials", [])
                    if permission_denials:
                        for denial in permission_denials:
                            if denial.get("tool_name") == "Write":
                                tool_input = denial.get("tool_input", {})
                                content = tool_input.get("content", "")
                                if content:
                                    logger.info("Extracted code from Write permission denial")
                                    return content

                    logger.error(f"No result or code found in response")
                    logger.error(f"Response keys: {response_data.keys()}")
                    logger.error(f"Response type: {response_data.get('type')}")
                    raise RuntimeError("No code generated in Claude response")
                else:
                    logger.error(f"Unexpected response type: {response_data.get('type')}")
                    logger.error(f"Full response: {json.dumps(response_data, indent=2)[:1000]}")
                    raise RuntimeError("Failed to extract result from Claude response")

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Raw output: {result.stdout[:500]}")
                raise RuntimeError(f"Invalid JSON response from Claude: {e}")

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

        args = ["claude"]

        if self.model:
            args.extend(["--model", self.model])

        for file_path in context_files:
            if Path(file_path).exists():
                args.extend(["--context", file_path])
            else:
                logger.warning(f"Context file not found: {file_path}")

        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.md',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(prompt)
            prompt_file = f.name

        try:
            args.extend(["--file", prompt_file])
            result = self.execute_command(args)
            return result.stdout
        finally:
            Path(prompt_file).unlink()
