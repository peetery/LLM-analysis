"""
Claude Code CLI Client.

This module implements a client for interacting with Claude Code via its
command-line interface. It uses the `-p` (print) flag for non-interactive
automation and JSON output format for reliable parsing.

Authentication:
    Automatic via Claude Pro/Team/Enterprise subscription.
    The parent Claude Code process handles all authentication.

Available Models:
    - claude-sonnet-4-5-20250929: Latest Claude Sonnet 4.5 (recommended)

Technical Details:
    - Uses JSON output format for structured responses
    - Prompts are written to temporary files for Windows compatibility
    - Supports Chain-of-Thought prompting via sequential execution
"""

import subprocess
import tempfile
import logging
import platform
import time
import json
from pathlib import Path
from typing import Optional, List

from .base_cli_client import BaseCLIClient

logger = logging.getLogger(__name__)


class ClaudeCodeClient(BaseCLIClient):
    """
    Client for Claude Code CLI tool.

    This client provides integration with Claude Code's command-line interface,
    enabling automated test generation experiments without manual interaction.

    Attributes:
        SUPPORTED_MODELS: List of valid model identifiers
        MODEL_ALIASES: Human-readable aliases for model identifiers
    """

    SUPPORTED_MODELS = [
        "claude-sonnet-4-5-20250929",
    ]

    MODEL_ALIASES = {
        "claude-sonnet-4.5": "claude-sonnet-4-5-20250929",
    }

    def __init__(self, model: str = "claude-sonnet-4.5", timeout: int = 300):
        """
        Initialize Claude Code client.

        Args:
            model: Model name or alias (default: 'claude-sonnet-4.5')
            timeout: Command timeout in seconds (default: 300)

        Raises:
            ValueError: If the specified model is not supported
            RuntimeError: If Claude CLI is not installed or not accessible
        """
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
            logger.warning(
                "Could not verify Claude authentication, proceeding anyway"
            )

        logger.info("Claude Code client initialized with model: %s", model)

    def check_installation(self) -> bool:
        """
        Verify Claude CLI installation.

        Returns:
            True if Claude CLI is installed and working, False otherwise
        """
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
                logger.error(
                    "Claude CLI returned error code %d",
                    result.returncode
                )
                logger.debug("stderr: %s", result.stderr[:200])
                return False

        except FileNotFoundError:
            logger.error("Claude CLI not found in PATH")
            return False
        except subprocess.TimeoutExpired:
            logger.error("Claude CLI test timed out after 30s")
            return False
        except Exception as e:
            logger.error("Error checking installation: %s", e)
            return False

    def check_authentication(self) -> bool:
        """
        Check Claude authentication status.

        Claude Code handles authentication automatically through the parent
        process, so this method always returns True.

        Returns:
            True (authentication is managed by parent process)
        """
        return True

    def send_prompt(self, prompt: str, **kwargs) -> str:
        """
        Send prompt to Claude Code and retrieve the response.

        This method uses the `-p --output-format json` flags for reliable
        non-interactive execution. Prompts are written to a temporary file
        to ensure proper handling on Windows where stdin can be unreliable.

        Args:
            prompt: The prompt text to send
            **kwargs: Additional arguments (currently unused)

        Returns:
            The model's response text

        Raises:
            RuntimeError: If the command fails or no valid response is received
        """
        logger.info("Sending prompt to Claude Code (%d chars)", len(prompt))

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
            logger.info("Claude Code response received in %.2fs", elapsed_time)

            if result.returncode != 0:
                logger.error(
                    "Command failed with return code %d",
                    result.returncode
                )
                logger.error("stderr: %s", result.stderr)
                logger.debug("stdout: %s", result.stdout[:500])
                raise RuntimeError(
                    f"Claude command failed. "
                    f"stderr: {result.stderr}, stdout: {result.stdout[:200]}"
                )

            try:
                response_data = json.loads(result.stdout)

                if response_data.get("type") == "result":
                    result_text = response_data.get("result", "")

                    if result_text:
                        logger.info(
                            "Received Claude response (%d chars)",
                            len(result_text)
                        )
                        self._log_code_detection(result_text)
                        return result_text

                    permission_denials = response_data.get(
                        "permission_denials", []
                    )
                    if permission_denials:
                        for denial in permission_denials:
                            if denial.get("tool_name") == "Write":
                                tool_input = denial.get("tool_input", {})
                                content = tool_input.get("content", "")
                                if content:
                                    logger.info(
                                        "Extracted code from Write permission denial"
                                    )
                                    return content

                    logger.error("No result or code found in response")
                    logger.debug("Response keys: %s", response_data.keys())
                    logger.debug("Response type: %s", response_data.get('type'))
                    raise RuntimeError("No code generated in Claude response")
                else:
                    logger.error(
                        "Unexpected response type: %s",
                        response_data.get('type')
                    )
                    logger.debug(
                        "Full response: %s",
                        json.dumps(response_data, indent=2)[:1000]
                    )
                    raise RuntimeError(
                        "Failed to extract result from Claude response"
                    )

            except json.JSONDecodeError as e:
                logger.error("Failed to parse JSON response: %s", e)
                logger.debug("Raw output: %s", result.stdout[:500])
                raise RuntimeError(f"Invalid JSON response from Claude: {e}")

        finally:
            Path(prompt_file).unlink(missing_ok=True)

    def _log_code_detection(self, text: str):
        """
        Log information about detected code in the response.

        Args:
            text: Response text to analyze
        """
        if '```python' in text:
            logger.debug("Response contains Python code blocks")
        elif '```' in text:
            logger.debug("Response contains generic code blocks")
        elif 'import unittest' in text or 'def test' in text:
            logger.debug("Response appears to be raw Python code")
        else:
            logger.warning("Response doesn't appear to contain code")

    def set_model(self, model: str):
        """
        Switch to a different model.

        Args:
            model: Model identifier

        Raises:
            ValueError: If the model is not supported
        """
        if model not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Unsupported model: {model}. "
                f"Supported models: {', '.join(self.SUPPORTED_MODELS)}"
            )

        self.model = model
        logger.info("Switched to model: %s", model)

    def get_available_models(self) -> List[str]:
        """
        Get list of available models.

        Returns:
            List of supported model identifiers
        """
        return self.SUPPORTED_MODELS.copy()

    def send_prompt_with_context(
        self,
        prompt: str,
        context_files: Optional[List[str]] = None
    ) -> str:
        """
        Send prompt with additional context files.

        This method allows providing source files as context to the model,
        which can improve test generation quality.

        Args:
            prompt: The prompt text
            context_files: List of file paths to include as context

        Returns:
            The model's response text
        """
        if not context_files:
            return self.send_prompt(prompt)

        logger.info(
            "Sending prompt with %d context files",
            len(context_files)
        )

        args = ["claude"]

        if self.model:
            args.extend(["--model", self.model])

        for file_path in context_files:
            if Path(file_path).exists():
                args.extend(["--context", file_path])
            else:
                logger.warning("Context file not found: %s", file_path)

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
            Path(prompt_file).unlink(missing_ok=True)
