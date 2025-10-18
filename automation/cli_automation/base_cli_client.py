"""
Base class for CLI-based LLM clients

This module provides the abstract base class for all CLI tool clients.
All CLI clients (Codex, Claude Code, Copilot, Gemini) inherit from this class.
"""

from abc import ABC, abstractmethod
import subprocess
import time
import logging
import platform
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class BaseCLIClient(ABC):
    """Abstract base class for CLI-based LLM clients"""

    def __init__(self, command: str, model: str = None, timeout: int = 300):
        """
        Initialize CLI client

        Args:
            command: CLI command to execute (e.g., 'codex', 'claude', 'copilot', 'gemini')
            model: Model name to use (optional, model-specific)
            timeout: Command timeout in seconds (default: 300s = 5min)
        """
        self.command = command
        self.model = model
        self.timeout = timeout
        self.last_response_time = 0

        logger.info(f"Initialized {self.__class__.__name__} with command='{command}', model='{model}'")

    @abstractmethod
    def send_prompt(self, prompt: str, **kwargs) -> str:
        """
        Send prompt to CLI tool and get response

        This is the main method that each CLI client must implement.
        It should execute the CLI command with the prompt and return the response.

        Args:
            prompt: The prompt text to send to the LLM
            **kwargs: Additional CLI-specific arguments

        Returns:
            Response text from the model

        Raises:
            RuntimeError: If the command fails after all retries
            subprocess.TimeoutExpired: If the command times out
        """
        pass

    @abstractmethod
    def check_installation(self) -> bool:
        """
        Check if CLI tool is installed and available

        Returns:
            True if CLI tool is installed, False otherwise
        """
        pass

    @abstractmethod
    def check_authentication(self) -> bool:
        """
        Check if user is authenticated to use the CLI tool

        Returns:
            True if authenticated, False otherwise
        """
        pass

    def execute_command(
        self,
        args: list,
        input_text: str = None,
        max_retries: int = 3,
        env: Dict[str, str] = None
    ) -> subprocess.CompletedProcess:
        """
        Execute CLI command with retries and error handling

        This method handles:
        - Multiple retry attempts with exponential backoff
        - Timeout handling
        - Error logging
        - Response time measurement

        Args:
            args: Command arguments as list (e.g., ['codex', '--stdin'])
            input_text: Text to send to stdin (optional)
            max_retries: Number of retry attempts (default: 3)
            env: Environment variables dict (optional)

        Returns:
            Completed subprocess result

        Raises:
            RuntimeError: If all retry attempts fail
        """
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                logger.info(f"Executing command (attempt {attempt + 1}/{max_retries}): {' '.join(args)}")

                # On Windows, use shell=True for better CMD/PowerShell compatibility
                result = subprocess.run(
                    args,
                    input=input_text,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    env=env,
                    shell=True if platform.system() == "Windows" else False
                )

                self.last_response_time = time.time() - start_time

                if result.returncode == 0:
                    logger.info(f"Command succeeded in {self.last_response_time:.2f}s")
                    logger.debug(f"Output length: {len(result.stdout)} chars")
                    return result
                else:
                    logger.warning(
                        f"Attempt {attempt + 1} failed with return code {result.returncode}"
                    )
                    logger.warning(f"stderr: {result.stderr}")  # Log full stderr for debugging

            except subprocess.TimeoutExpired:
                logger.warning(f"Attempt {attempt + 1} timed out after {self.timeout}s")

            except FileNotFoundError:
                logger.error(f"Command not found: {args[0]}")
                raise RuntimeError(f"CLI tool '{args[0]}' not found. Is it installed?")

            except Exception as e:
                logger.error(f"Attempt {attempt + 1} error: {e}")

            # Exponential backoff between retries
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.info(f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)

        raise RuntimeError(f"All {max_retries} attempts failed for command: {' '.join(args)}")

    def get_version(self) -> Optional[str]:
        """
        Get version of the CLI tool

        Returns:
            Version string or None if unavailable
        """
        try:
            result = subprocess.run(
                [self.command, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception as e:
            logger.warning(f"Could not get version: {e}")
            return None

    def cleanup(self):
        """
        Cleanup resources

        For CLI clients, this is usually a no-op since subprocess handles cleanup.
        Override this method if your client needs specific cleanup.
        """
        logger.debug(f"Cleanup called for {self.__class__.__name__}")
        pass

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()
        return False  # Don't suppress exceptions

    def __repr__(self):
        """String representation"""
        return f"{self.__class__.__name__}(command='{self.command}', model='{self.model}')"
