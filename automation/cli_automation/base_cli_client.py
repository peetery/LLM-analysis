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
import time as time_module
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class BaseCLIClient(ABC):
    """Abstract base class for CLI-based LLM clients"""

    def __init__(self, command: str, model: str = None, timeout: int = 300):
        self.command = command
        self.model = model
        self.timeout = timeout
        self.last_response_time = 0

        logger.info(f"Initialized {self.__class__.__name__} with command='{command}', model='{model}'")

    def send_prompts_sequential(self, prompts: list) -> tuple:
        logger.info(f"🔄 Chain of Thought (CLI simulation): {len(prompts)} steps")
        logger.info(f"   Building conversation context step-by-step...")

        responses = []
        conversation_history = ""
        total_time = 0

        for i, current_prompt in enumerate(prompts):
            step_num = i + 1
            is_final_step = (i == len(prompts) - 1)
            logger.info(f"\n📝 Step {step_num}/{len(prompts)}")

            if conversation_history:
                full_input = f"{conversation_history}\n\n{current_prompt}"
                logger.info(f"   Sending prompt with {len(conversation_history)} chars of history")
            else:
                full_input = current_prompt
                logger.info(f"   Sending initial prompt ({len(current_prompt)} chars)")

            start = time_module.time()

            response = self.send_prompt(full_input, is_final_step=is_final_step)
            elapsed = time_module.time() - start
            total_time += elapsed

            if not response:
                raise RuntimeError(f"CoT Step {step_num} failed - no response")

            logger.info(f"   ✓ Step {step_num} completed in {elapsed:.2f}s ({len(response)} chars)")
            responses.append(response)

            conversation_history += f"{current_prompt}\n\n{response}\n\n"

            if i < len(prompts) - 1:
                time_module.sleep(1)

        final_response = responses[-1] if responses else ""
        logger.info(f"\n✅ Chain of Thought completed: {len(responses)} steps in {total_time:.2f}s")

        return responses, final_response, total_time

    @abstractmethod
    def send_prompt(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    def check_installation(self) -> bool:
        pass

    @abstractmethod
    def check_authentication(self) -> bool:
        pass

    def execute_command(
        self,
        args: list,
        input_text: str = None,
        max_retries: int = 3,
        env: Dict[str, str] = None
    ) -> subprocess.CompletedProcess:
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                logger.info(f"Executing command (attempt {attempt + 1}/{max_retries}): {' '.join(args)}")

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
                    logger.warning(f"stderr: {result.stderr}")

            except subprocess.TimeoutExpired:
                logger.warning(f"Attempt {attempt + 1} timed out after {self.timeout}s")

            except FileNotFoundError:
                logger.error(f"Command not found: {args[0]}")
                raise RuntimeError(f"CLI tool '{args[0]}' not found. Is it installed?")

            except Exception as e:
                logger.error(f"Attempt {attempt + 1} error: {e}")

            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.info(f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)

        raise RuntimeError(f"All {max_retries} attempts failed for command: {' '.join(args)}")

    def get_version(self) -> Optional[str]:
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
        logger.debug(f"Cleanup called for {self.__class__.__name__}")
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}(command='{self.command}', model='{self.model}')"
