"""
Prompting Strategies for LLM Test Generation.

This module defines different prompting strategies for automated unit test
generation. It provides a framework for loading and executing prompt templates
with different levels of code context and prompting approaches.

Available Strategies:
    - SimplePrompting: Single-step prompt requesting complete test suite
    - ChainOfThoughtPrompting: Multi-step process (analyze → plan → implement)

Supported Context Levels:
    - interface: Method signatures only
    - interface_docstring: Signatures with docstrings
    - full_context: Complete source code implementation

Modes:
    - Legacy mode: Uses static prompt files from prompts_results/ (OrderCalculator)
    - Universal mode: Uses ClassContextExtractor for dynamic prompt generation
"""

import time
import logging
from pathlib import Path
from typing import Dict, Optional, TYPE_CHECKING

# Import for type hints only to avoid circular imports
if TYPE_CHECKING:
    from class_context_extractor import ClassContextExtractor

logger = logging.getLogger(__name__)


class PromptStrategy:
    """
    Abstract base class for prompting strategies.

    This class handles loading prompt templates from the filesystem
    and provides common functionality for all strategies.

    Supports two modes:
    - Legacy mode (extractor=None): Loads prompts from prompts_results/
    - Universal mode (extractor provided): Generates prompts dynamically

    Attributes:
        base_path (Path): Root directory containing prompt templates
        prompts (Dict): Cached prompt templates
        extractor: ClassContextExtractor for universal mode (or None for legacy)
        template_manager: PromptTemplateManager for universal mode
    """

    def __init__(self, base_path=None, extractor: Optional['ClassContextExtractor'] = None):
        """
        Initialize the prompt strategy.

        Args:
            base_path: Path to prompts_results directory (legacy mode)
            extractor: ClassContextExtractor instance (universal mode)
        """
        self.extractor = extractor
        self.template_manager = None

        # Initialize template manager for universal mode
        if extractor is not None:
            from prompt_templates import PromptTemplateManager
            self.template_manager = PromptTemplateManager()
            logger.info(f"Universal mode: using extractor for {extractor.class_name}")
        else:
            logger.info("Legacy mode: using static prompts from prompts_results/")

        # Initialize legacy mode path resolution
        if base_path is None:
            current_file = Path(__file__).parent
            self.base_path = current_file.parent / "prompts_results"

            if not self.base_path.exists():
                logger.warning(f"Base path {self.base_path} doesn't exist, trying alternative paths")
                alternatives = [
                    Path.cwd().parent / "prompts_results",
                    Path.cwd() / ".." / "prompts_results",
                    current_file.parent.parent / "prompts_results"
                ]

                for alt_path in alternatives:
                    if alt_path.exists():
                        self.base_path = alt_path.resolve()
                        logger.info(f"Found prompts_results at: {self.base_path}")
                        break
                else:
                    if extractor is None:
                        logger.error(f"Could not find prompts_results directory in any of: {[str(p) for p in alternatives]}")
        else:
            self.base_path = Path(base_path)

        self.load_prompts()

    def load_prompts(self):
        self.prompts = {}

        if self.extractor is not None:
            # Universal mode - no need to load static prompts
            return

        if not self.base_path.exists():
            logger.warning(f"Directory {self.base_path} does not exist!")
            return

        logger.info(f"Prompt base path: {self.base_path}")

    def load_specific_prompt(self, strategy, context):
        """Load a specific prompt from file (legacy mode only)."""
        if strategy == "simple_prompting":
            key = context
            prompt_file = self.base_path / "simple_prompting" / context / "prompt.txt"
        else:  # chain_of_thought_prompting
            key = f"cot_{context}"
            prompt_file = self.base_path / "chain_of_thought_prompting" / context / "prompt.txt"

        logger.info(f"Looking for prompt: {strategy}/{context} at {prompt_file}")
        logger.info(f"Base path: {self.base_path}")
        logger.info(f"File exists: {prompt_file.exists()}")

        if key not in self.prompts:
            if prompt_file.exists():
                try:
                    self.prompts[key] = prompt_file.read_text(encoding='utf-8')
                    logger.info(f"Loaded prompt: {strategy}/{context} ({len(self.prompts[key])} chars)")
                except Exception as e:
                    logger.error(f"Error reading prompt file {prompt_file}: {e}")
                    return None
            else:
                logger.error(f"Prompt not found: {prompt_file}")
                if prompt_file.parent.exists():
                    available_files = list(prompt_file.parent.iterdir())
                    logger.error(f"Available files in {prompt_file.parent}: {[f.name for f in available_files]}")
                return None

        return self.prompts.get(key)

    def parse_cot_content(self, content):
        """Parse CoT content into steps (legacy mode)."""
        steps = {}
        parts = content.split('\n\n')

        current_step = None
        current_content = []

        for part in parts:
            part = part.strip()
            if part.startswith('1)'):
                if current_step:
                    steps[current_step] = '\n\n'.join(current_content)
                current_step = 'step1'
                current_content = [part[2:].strip()]
            elif part.startswith('2)'):
                if current_step:
                    steps[current_step] = '\n\n'.join(current_content)
                current_step = 'step2'
                current_content = [part[2:].strip()]
            elif part.startswith('3)'):
                if current_step:
                    steps[current_step] = '\n\n'.join(current_content)
                current_step = 'step3'
                current_content = [part[2:].strip()]
            elif current_step:
                current_content.append(part)

        if current_step and current_content:
            steps[current_step] = '\n\n'.join(current_content)

        return steps

    def get_context_content(self, context_type):
        """Get context content (universal or legacy mode)."""
        if self.extractor is not None:
            return self.extractor.extract_context(context_type)

        # Legacy mode
        if context_type == "interface":
            return self.get_interface_only()
        elif context_type == "interface_docstring":
            return self.get_interface_with_docstrings()
        elif context_type == "full_context":
            return self.get_full_context()
        else:
            raise ValueError(f"Unknown context type: {context_type}")

    def get_interface_only(self):
        """Legacy mode: hardcoded interface for OrderCalculator."""
        return '''class OrderCalculator:
    def __init__(self, tax_rate=0.08, shipping_cost=5.0):
        pass

    def calculate_subtotal(self, items):
        pass

    def calculate_tax(self, subtotal):
        pass

    def calculate_shipping(self, items, subtotal):
        pass

    def apply_discount(self, subtotal, discount_code=None):
        pass

    def calculate_total(self, items, discount_code=None):
        pass'''

    def get_interface_with_docstrings(self):
        """Legacy mode: read order_calculator.py file."""
        order_calc_path = Path("order_calculator.py")
        if order_calc_path.exists():
            content = order_calc_path.read_text()
            return content
        return self.get_interface_only()

    def get_full_context(self):
        """Legacy mode: read order_calculator.py file."""
        order_calc_path = Path("order_calculator.py")
        if order_calc_path.exists():
            return order_calc_path.read_text()
        return ""

    def _get_placeholders(self, context_type):
        """Create placeholders for template substitution (universal mode)."""
        from prompt_templates import create_placeholders_from_extractor
        return create_placeholders_from_extractor(self.extractor, context_type)


class SimplePrompting(PromptStrategy):
    """
    Simple prompting strategy: single prompt requesting complete test suite.
    """

    def execute(self, llm_client, context_type):
        """
        Execute simple prompting strategy.

        Args:
            llm_client: LLM client to send prompts to
            context_type: One of 'interface', 'interface_docstring', 'full_context'

        Returns:
            Dictionary with response, timing, and metadata
        """
        logger.info(f"Executing simple prompting strategy for {context_type}")

        # Generate prompt based on mode
        if self.extractor is not None:
            # Universal mode - dynamic prompt generation
            placeholders = self._get_placeholders(context_type)
            final_prompt = self.template_manager.get_simple_prompt(placeholders)
            logger.info(f"Generated dynamic prompt for {self.extractor.class_name}")
        else:
            # Legacy mode - load from file
            final_prompt = self.load_specific_prompt("simple_prompting", context_type)
            if not final_prompt:
                logger.error(f"No prompt template found for simple_prompting/{context_type}")
                return None

        response = llm_client.send_prompt(final_prompt)
        response_time = getattr(llm_client, 'last_response_time', 0)

        if response:
            logger.info(f"Simple prompting completed in {response_time:.2f}s")
            return {
                'response': response,
                'response_time': response_time,
                'strategy': 'simple_prompting',
                'context_type': context_type,
                'prompt': final_prompt
            }

        return None


class ChainOfThoughtPrompting(PromptStrategy):
    """
    Chain-of-thought prompting strategy: multi-step process.

    Steps:
        1. Analyze the class to understand its behavior
        2. Plan test scenarios
        3. Generate the test code
    """

    def __init__(self, base_path=None, extractor: Optional['ClassContextExtractor'] = None):
        super().__init__(base_path, extractor)
        if self.extractor is None:
            self.cot_prompts = self.parse_cot_prompts()

    def parse_cot_prompts(self):
        """Check which CoT prompts are available (legacy mode)."""
        cot_prompts = {}

        for context in ['interface', 'interface_docstring', 'full_context']:
            prompt_file = self.base_path / "chain_of_thought_prompting" / context / "prompt.txt"
            if prompt_file.exists():
                logger.info(f"Found CoT prompt file for {context}: {prompt_file}")
                cot_prompts[context] = True
            else:
                logger.warning(f"Missing CoT prompt file for {context}: {prompt_file}")

        return cot_prompts

    def execute(self, llm_client, context_type):
        """
        Execute chain-of-thought prompting strategy.

        Args:
            llm_client: LLM client to send prompts to
            context_type: One of 'interface', 'interface_docstring', 'full_context'

        Returns:
            Dictionary with responses, timing, and metadata
        """
        logger.info(f"Executing chain-of-thought prompting for {context_type}")

        # Get steps based on mode
        if self.extractor is not None:
            # Universal mode - dynamic prompt generation
            placeholders = self._get_placeholders(context_type)
            steps = self.template_manager.get_cot_prompts(placeholders)
            logger.info(f"Generated dynamic CoT prompts for {self.extractor.class_name}")
        else:
            # Legacy mode - load and parse from file
            cot_content = self.load_specific_prompt("chain_of_thought_prompting", context_type)
            if not cot_content:
                logger.error(f"No CoT prompt found for {context_type}")
                return None

            steps = self.parse_cot_content(cot_content)
            if not steps:
                logger.error(f"Could not parse CoT steps from prompt")
                return None

        is_cli_client = hasattr(llm_client, 'command')

        if is_cli_client:
            return self._execute_cli_mode(llm_client, steps, context_type)
        else:
            return self._execute_web_mode(llm_client, steps, context_type)

    def _execute_cli_mode(self, llm_client, steps, context_type):
        """Execute CoT in CLI mode (sequential prompts)."""
        logger.info("CLI mode detected: using sequential prompts with context passing")

        prompt_list = [
            steps.get('step1', ''),
            steps.get('step2', ''),
            steps.get('step3', '')
        ]

        if not hasattr(llm_client, 'send_prompts_sequential'):
            logger.error("CLI client doesn't support send_prompts_sequential method")
            return None

        try:
            responses, final_response, total_time = llm_client.send_prompts_sequential(prompt_list)

            logger.info(f"Chain-of-thought completed in {total_time:.2f}s (sequential with context)")

            return {
                'responses': [
                    {'step': i+1, 'prompt': prompt_list[i], 'response': responses[i], 'response_time': 0}
                    for i in range(len(responses))
                ],
                'final_response': final_response,
                'total_response_time': total_time,
                'strategy': 'chain_of_thought_prompting',
                'context_type': context_type
            }
        except Exception as e:
            logger.error(f"Sequential CoT failed: {e}", exc_info=True)
            return None

    def _execute_web_mode(self, llm_client, steps, context_type):
        """Execute CoT in web automation mode (conversational)."""
        logger.info("Web automation mode: sending 3 prompts sequentially (conversational)")
        total_time = 0
        responses = []

        step_names = ['Code analysis', 'Test strategy', 'Code generation']

        for i, step_key in enumerate(['step1', 'step2', 'step3']):
            logger.info(f"Step {i+1}: {step_names[i]}")
            prompt = steps.get(step_key, '')
            if not prompt:
                logger.error(f"No {step_key} prompt found")
                return None

            skip_verification = (i > 0)  # Only verify on first step
            response = llm_client.send_prompt(prompt, skip_model_verification=skip_verification)
            step_time = getattr(llm_client, 'last_response_time', 0)
            total_time += step_time

            if not response:
                logger.error(f"Failed at step {i+1}")
                return None

            responses.append({
                'step': i+1,
                'prompt': prompt,
                'response': response,
                'response_time': step_time
            })

            if i < 2:  # Don't sleep after last step
                time.sleep(2)

        logger.info(f"Chain-of-thought completed in {total_time:.2f}s")

        return {
            'responses': responses,
            'final_response': responses[-1]['response'],
            'total_response_time': total_time,
            'strategy': 'chain_of_thought_prompting',
            'context_type': context_type
        }
