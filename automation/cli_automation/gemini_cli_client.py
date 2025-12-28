"""
Gemini CLI Client.

This module implements a client for interacting with Google's Gemini models
via the Gemini CLI tool. It uses the `-p` (prompt) flag for non-interactive
automation and JSON output format for reliable parsing.

Authentication:
    Option 1 (Recommended): Login via Google Account
        Run: gemini login
    Option 2: Use API key via GEMINI_API_KEY environment variable
        export GEMINI_API_KEY=your_api_key

Available Models:
    - gemini-3-pro: Gemini 3 Pro (newest, most capable, preview)
    - gemini-3-flash: Gemini 3 Flash (newest, fast, preview)
    - gemini-2.5-pro: Gemini 2.5 Pro (stable, general availability)
    - gemini-2.5-flash: Gemini 2.5 Flash (fast, general availability)
    - gemini-2.0-flash: Gemini 2.0 Flash (legacy)

Note: Gemini 3 Pro requires Preview Features enabled in /settings
      and Google AI Ultra subscription or paid API key.

Technical Details:
    - Uses JSON output format (-o json) for structured responses
    - Prompts are piped via stdin (Gemini CLI 0.19+ deprecated -p flag)
    - Uses --yolo flag for non-interactive execution
"""

import subprocess
import tempfile
import logging
import platform
import time
import json
import os
from pathlib import Path
from typing import Optional, List

from .base_cli_client import BaseCLIClient

logger = logging.getLogger(__name__)


class GeminiCLIClient(BaseCLIClient):
    """
    Client for Gemini CLI tool.

    This client provides integration with Google's Gemini CLI,
    enabling automated test generation experiments with Gemini models.

    Attributes:
        SUPPORTED_MODELS: List of valid model identifiers
        MODEL_ALIASES: Human-readable aliases for model identifiers
    """

    SUPPORTED_MODELS = [
        "gemini-3-pro-preview",
        "gemini-3-flash-preview",
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
    ]

    MODEL_ALIASES = {
        "gemini-3-pro": "gemini-3-pro-preview",  # Alias for convenience
        "gemini-3-pro-preview": "gemini-3-pro-preview",
        "gemini-3-flash": "gemini-3-flash-preview",  # Alias for convenience
        "gemini-3-flash-preview": "gemini-3-flash-preview",
        "gemini-2.5-pro": "gemini-2.5-pro",
        "gemini-2.5-flash": "gemini-2.5-flash",
        "gemini-2.0-flash": "gemini-2.0-flash",
    }

    def __init__(self, model: str = "gemini-2.5-flash", timeout: int = 300):
        """
        Initialize Gemini CLI client.

        Args:
            model: Model name or alias (default: 'gemini-2.5-flash')
            timeout: Command timeout in seconds (default: 300)

        Raises:
            ValueError: If the specified model is not supported
            RuntimeError: If Gemini CLI is not installed or not accessible
        """
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

        logger.info("Gemini CLI client initialized with model: %s", model)

    def check_installation(self) -> bool:
        """
        Verify Gemini CLI installation.

        Returns:
            True if Gemini CLI is installed and working, False otherwise
        """
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
                logger.info("Gemini CLI is installed: %s", version)
                return True
            else:
                logger.error(
                    "Gemini CLI returned error code %d",
                    result.returncode
                )
                return False

        except FileNotFoundError:
            logger.error("Gemini CLI not found in PATH")
            logger.error("Install with: npm install -g @google/gemini-cli")
            return False
        except subprocess.TimeoutExpired:
            logger.error("Gemini CLI version check timed out")
            return False
        except Exception as e:
            logger.error("Error checking installation: %s", e)
            return False

    def check_authentication(self) -> bool:
        """
        Check Gemini authentication status.

        This method checks for GEMINI_API_KEY environment variable.
        If not found, it assumes the user is logged in via 'gemini login'.

        Returns:
            True if authentication is configured
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            logger.info("GEMINI_API_KEY environment variable found")
            return True

        logger.debug(
            "No GEMINI_API_KEY found, assuming logged in via 'gemini login'"
        )
        logger.debug("If not logged in, run: gemini login")
        return True

    def send_prompt(self, prompt: str, **kwargs) -> str:
        """
        Send prompt to Gemini CLI and retrieve the response.

        This method pipes the prompt via stdin and uses `-o json --yolo` flags
        for reliable non-interactive execution. The --yolo flag auto-approves
        all actions to avoid interactive prompts.

        For Chain-of-Thought prompting, the is_final_step parameter can be
        passed to add instructions for returning code.

        Args:
            prompt: The prompt text to send
            **kwargs: Additional arguments
                - is_final_step (bool): If True, adds instruction to return code

        Returns:
            The model's response text

        Raises:
            RuntimeError: If the command fails or no valid response is received
        """
        logger.info("Sending prompt to Gemini CLI (%d chars)", len(prompt))

        is_final_step = kwargs.get('is_final_step', True)

        if is_final_step:
            enhanced_prompt = f"""{prompt}

IMPORTANT: Return the complete code in your response. Do NOT use write_file, edit_file, or any other tools. Just provide the code directly in your answer."""
        else:
            enhanced_prompt = prompt
            logger.debug(
                "Skipping 'return code' instruction (not final step)"
            )

        start_time = time.time()

        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.txt',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(enhanced_prompt)
            prompt_file = f.name

        try:
            # Gemini CLI 0.19+ uses positional prompt instead of -p flag
            # Use stdin piping with type (Windows) or cat (Linux)
            if platform.system() == "Windows":
                pipe_cmd = f'type "{prompt_file}"'
            else:
                pipe_cmd = f'cat "{prompt_file}"'

            cmd_parts = [
                self.command,
                '-o', 'json',  # Output format (short flag)
                '--yolo'  # Auto-approve to avoid interactive prompts
            ]

            if self.model:
                cmd_parts.extend(['-m', self.model])

            cmd_str = f'{pipe_cmd} | {" ".join(cmd_parts)}'

            result = subprocess.run(
                cmd_str,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                shell=True
            )

            elapsed_time = time.time() - start_time
            self.last_response_time = elapsed_time
            logger.info("Gemini CLI response received in %.2fs", elapsed_time)

            if result.returncode != 0:
                logger.error(
                    "Command failed with return code %d",
                    result.returncode
                )
                logger.error("stderr: %s", result.stderr)
                logger.debug("stdout: %s", result.stdout[:500])
                raise RuntimeError(
                    f"Gemini command failed. "
                    f"stderr: {result.stderr}, stdout: {result.stdout[:200]}"
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
                    logger.info(
                        "Received Gemini response (%d chars)",
                        len(result_text)
                    )
                    self._log_code_detection(result_text)
                    return result_text

                logger.error("Could not extract result from JSON response")
                logger.debug(
                    "Response keys: %s",
                    list(response_data.keys()) if isinstance(response_data, dict)
                    else 'not a dict'
                )
                logger.debug(
                    "Response structure: %s",
                    json.dumps(response_data, indent=2)[:1000]
                )
                raise RuntimeError("No code generated in Gemini response")

            except json.JSONDecodeError as e:
                logger.error("Failed to parse JSON response: %s", e)
                logger.debug("Raw output: %s", result.stdout[:500])

                if 'import unittest' in result.stdout or 'def test' in result.stdout:
                    logger.info("Fallback: treating raw output as code")
                    return result.stdout

                raise RuntimeError(f"Invalid JSON response from Gemini: {e}")

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

        Note: Context file support is not yet implemented for Gemini CLI.
        This method falls back to regular prompt sending.

        Args:
            prompt: The prompt text
            context_files: List of file paths to include as context (not used)

        Returns:
            The model's response text
        """
        if not context_files:
            return self.send_prompt(prompt)

        logger.info(
            "Sending prompt with %d context files",
            len(context_files)
        )
        logger.warning("Context files not yet implemented for Gemini CLI")

        return self.send_prompt(prompt)
