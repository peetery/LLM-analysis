"""
Base class for CLI-based LLM clients.

This module provides the abstract base class for all CLI tool clients.
All CLI clients (Claude Code, Gemini CLI, etc.) inherit from this class
and implement the required abstract methods.

The base class handles:
    - Command execution with retry logic
    - Timeout handling
    - Sequential prompt execution for Chain-of-Thought
    - Context manager protocol for resource cleanup
"""

from abc import ABC, abstractmethod
import subprocess
import time
import logging
import platform
from typing import Optional, Dict, Any, List, Tuple

logger = logging.getLogger(__name__)


class BaseCLIClient(ABC):
    """
    Abstract base class for CLI-based Large Language Model clients.

    This class provides common functionality for interacting with LLM CLI tools,
    including command execution, retry logic, and sequential prompt handling
    for Chain-of-Thought prompting strategies.

    Attributes:
        command (str): CLI command name (e.g., 'claude', 'gemini')
        model (str): Model identifier for the LLM
        timeout (int): Maximum execution time in seconds for CLI commands
        last_response_time (float): Time taken for the last response in seconds
    """

    def __init__(self, command: str, model: Optional[str] = None, timeout: int = 300):
        """
        Initialize the CLI client.

        Args:
            command: Name of the CLI command to execute
            model: Model identifier (e.g., 'claude-sonnet-4.5')
            timeout: Command timeout in seconds (default: 300)
        """
        self.command = command
        self.model = model
        self.timeout = timeout
        self.last_response_time = 0

        logger.info(
            "Initialized %s with command='%s', model='%s'",
            self.__class__.__name__, command, model
        )

    def send_prompts_sequential(
        self,
        prompts: List[str]
    ) -> Tuple[List[str], str, float]:
        """
        Execute multiple prompts sequentially, building conversation context.

        This method is used for Chain-of-Thought prompting, where each step
        builds upon the previous responses. The conversation history is passed
        to each subsequent prompt to maintain context.

        Args:
            prompts: List of prompt strings to execute in sequence

        Returns:
            Tuple containing:
                - List of response strings (one per prompt)
                - Final response string (last in the list)
                - Total execution time in seconds

        Raises:
            RuntimeError: If any step fails to produce a response
        """
        logger.info(
            "Chain of Thought execution: %d steps",
            len(prompts)
        )
        logger.debug("Building conversation context step-by-step")

        responses = []
        conversation_history = ""
        total_time = 0

        for i, current_prompt in enumerate(prompts):
            step_num = i + 1
            is_final_step = (i == len(prompts) - 1)

            logger.info("Executing step %d/%d", step_num, len(prompts))

            if conversation_history:
                full_input = f"{conversation_history}\n\n{current_prompt}"
                logger.debug(
                    "Sending prompt with %d chars of history",
                    len(conversation_history)
                )
            else:
                full_input = current_prompt
                logger.debug(
                    "Sending initial prompt (%d chars)",
                    len(current_prompt)
                )

            start = time.time()
            response = self.send_prompt(full_input, is_final_step=is_final_step)
            elapsed = time.time() - start
            total_time += elapsed

            if not response:
                raise RuntimeError(
                    f"Chain-of-Thought step {step_num} failed - no response received"
                )

            logger.info(
                "Step %d completed in %.2fs (%d chars)",
                step_num, elapsed, len(response)
            )
            responses.append(response)

            conversation_history += f"{current_prompt}\n\n{response}\n\n"

            if i < len(prompts) - 1:
                time.sleep(1)

        final_response = responses[-1] if responses else ""
        logger.info(
            "Chain-of-Thought completed: %d steps in %.2fs",
            len(responses), total_time
        )

        return responses, final_response, total_time

    @abstractmethod
    def send_prompt(self, prompt: str, **kwargs) -> str:
        """
        Send a single prompt to the LLM and retrieve the response.

        This method must be implemented by subclasses to handle
        the specific CLI tool's interface and response format.

        Args:
            prompt: The prompt text to send
            **kwargs: Additional arguments specific to the implementation

        Returns:
            The model's response as a string

        Raises:
            RuntimeError: If the command fails
        """
        pass

    @abstractmethod
    def check_installation(self) -> bool:
        """
        Verify that the CLI tool is installed and accessible.

        Returns:
            True if the tool is installed and working, False otherwise
        """
        pass

    @abstractmethod
    def check_authentication(self) -> bool:
        """
        Verify that the user is authenticated to use the CLI tool.

        Returns:
            True if authenticated, False otherwise
        """
        pass

    def execute_command(
        self,
        args: List[str],
        input_text: Optional[str] = None,
        max_retries: int = 3,
        env: Optional[Dict[str, str]] = None
    ) -> subprocess.CompletedProcess:
        """
        Execute a CLI command with retry logic and timeout handling.

        This method provides robust command execution with exponential backoff
        for retries. It handles platform-specific differences (Windows vs Unix).

        Args:
            args: List of command arguments
            input_text: Optional stdin input
            max_retries: Maximum number of retry attempts (default: 3)
            env: Optional environment variables

        Returns:
            CompletedProcess object containing the command results

        Raises:
            RuntimeError: If all retry attempts fail
        """
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                logger.debug(
                    "Executing command (attempt %d/%d): %s",
                    attempt + 1, max_retries, ' '.join(args)
                )

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
                    logger.debug(
                        "Command succeeded in %.2fs (output: %d chars)",
                        self.last_response_time, len(result.stdout)
                    )
                    return result
                else:
                    logger.warning(
                        "Attempt %d failed with return code %d",
                        attempt + 1, result.returncode
                    )
                    logger.debug("stderr: %s", result.stderr)

            except subprocess.TimeoutExpired:
                logger.warning(
                    "Attempt %d timed out after %ds",
                    attempt + 1, self.timeout
                )

            except FileNotFoundError:
                logger.error("Command not found: %s", args[0])
                raise RuntimeError(
                    f"CLI tool '{args[0]}' not found. Is it installed?"
                )

            except Exception as e:
                logger.error("Attempt %d error: %s", attempt + 1, e)

            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.info("Waiting %ds before retry...", wait_time)
                time.sleep(wait_time)

        raise RuntimeError(
            f"All {max_retries} attempts failed for command: {' '.join(args)}"
        )

    def get_version(self) -> Optional[str]:
        """
        Retrieve the CLI tool version.

        Returns:
            Version string if available, None otherwise
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
            logger.debug("Could not get version: %s", e)
            return None

    def cleanup(self):
        """
        Perform cleanup operations when the client is closed.

        This method can be overridden by subclasses to implement
        specific cleanup logic (e.g., closing connections, deleting temp files).
        """
        logger.debug("Cleanup called for %s", self.__class__.__name__)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.cleanup()
        return False

    def __repr__(self):
        """String representation of the client."""
        return (
            f"{self.__class__.__name__}"
            f"(command='{self.command}', model='{self.model}')"
        )
