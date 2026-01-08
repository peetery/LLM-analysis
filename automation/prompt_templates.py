"""
Prompt Template Manager for Universal Test Generation.

This module manages prompt templates with placeholders that are dynamically
filled based on the analyzed class. It supports both simple prompting and
chain-of-thought prompting strategies.

Available placeholders:
    {class_name}         - Name of the class being tested
    {module_name}        - Name of the module (without .py)
    {import_statement}   - Ready-to-use import statement
    {context_code}       - Extracted context (interface/docstring/full)
    {context_level}      - Human-readable context level description
    {helper_types}       - Description of helper types if any
    {public_methods_list} - Comma-separated list of public methods
"""

from dataclasses import dataclass
from typing import Dict, Optional
from pathlib import Path


@dataclass
class PromptPlaceholders:
    """
    Container for all placeholders available in prompt templates.

    All fields are strings that will be substituted into templates.
    """
    class_name: str
    module_name: str
    import_statement: str
    context_code: str
    context_level: str
    helper_types: str
    public_methods_list: str


# Template content as string constants
# These match the structure of existing prompts but with placeholders

SIMPLE_PROMPTING_TEMPLATE = '''Generate a complete Python unit test suite for the class `{class_name}`.

Instructions:
- Use the `unittest` framework.
- Include tests for all public methods of the class.
- Ensure proper coverage of:
  • typical use cases,
  • edge cases (corner cases),
  • incorrect input (invalid types or values),
  • exceptions.
- Each test should be clear, minimal and atomic (test one behavior at a time).
- Avoid comments or explanations — output only the test code.
- Return a single valid Python file with a class extending `unittest.TestCase`.
- IMPORTANT: Do NOT copy or redefine the {class_name} class in your test file.
  The class already exists in a separate module.
  Simply import it using: `{import_statement}`

Below is the {context_level} of the class:

```python
{context_code}
```'''


COT_STEP1_TEMPLATE = '''You are a software testing assistant. Your task is to generate a set of unit tests for a Python class provided below.

The tests should:
- use the `unittest` framework,
- cover all public methods,
- test typical usage as well as edge cases, invalid inputs, and exceptions,
- be clear, atomic, and minimal.

You will now analyze the class to prepare relevant test cases.
Do not write test code yet.

Below is the {context_level} of the class `{class_name}`:

```python
{context_code}
```'''


COT_STEP2_TEMPLATE = '''Based on the class above, list all relevant unit test scenarios you would create.
Each scenario should describe:
- the method being tested,
- the type of case (e.g. normal use, invalid input, exception),
- a short explanation of the intent.
List as many scenarios as you can think of, covering all aspects of the class.
Do not write test code yet.'''


COT_STEP3_TEMPLATE = '''Now, based on the test scenarios you just listed, generate the complete Python unit test suite using the `unittest` framework.

Follow these rules:
- Include one test method per scenario.
- Use meaningful test method names.
- Do not include comments or explanations.
- Output a valid `.py` file containing only the test class.
- IMPORTANT: Do NOT copy or redefine the {class_name} class in your test file.
  The class already exists in a separate module.
  Simply import it using: `{import_statement}`

The output must contain only Python code.'''


# Combined CoT template (for file-based prompts format)
COT_COMBINED_TEMPLATE = '''1)
{step1}


2)
{step2}



3)
{step3}'''


class PromptTemplateManager:
    """
    Manages prompt templates with dynamic placeholder substitution.

    This class provides methods to generate prompts for different strategies
    (simple_prompting, chain_of_thought_prompting) by filling in templates
    with class-specific information.

    Usage:
        manager = PromptTemplateManager()
        placeholders = PromptPlaceholders(
            class_name="OrderCalculator",
            module_name="order_calculator",
            ...
        )
        prompt = manager.get_simple_prompt(placeholders)
    """

    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize the template manager.

        Args:
            templates_dir: Optional directory containing custom templates.
                          If not provided, uses built-in templates.
        """
        self.templates_dir = templates_dir
        self._templates: Dict[str, str] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        """Load templates from directory or use built-in defaults."""
        # Use built-in templates by default
        self._templates = {
            'simple': SIMPLE_PROMPTING_TEMPLATE,
            'cot_step1': COT_STEP1_TEMPLATE,
            'cot_step2': COT_STEP2_TEMPLATE,
            'cot_step3': COT_STEP3_TEMPLATE,
        }

        # If custom templates directory provided, load from files
        if self.templates_dir and self.templates_dir.exists():
            self._load_templates_from_dir()

    def _load_templates_from_dir(self) -> None:
        """Load templates from the templates directory."""
        # Simple prompting template
        simple_template = self.templates_dir / "simple_prompting" / "template.txt"
        if simple_template.exists():
            self._templates['simple'] = simple_template.read_text(encoding='utf-8')

        # CoT templates
        cot_dir = self.templates_dir / "chain_of_thought_prompting"
        if cot_dir.exists():
            for step in ['step1_analyze', 'step2_plan', 'step3_generate']:
                step_file = cot_dir / f"{step}.txt"
                if step_file.exists():
                    key = step.replace('_analyze', '').replace('_plan', '').replace('_generate', '')
                    self._templates[f'cot_{key}'] = step_file.read_text(encoding='utf-8')

    def render_template(self, template_name: str, placeholders: PromptPlaceholders) -> str:
        """
        Render a template with the given placeholders.

        Args:
            template_name: Name of the template to render
            placeholders: Placeholder values to substitute

        Returns:
            Rendered template string

        Raises:
            KeyError: If template not found
        """
        if template_name not in self._templates:
            raise KeyError(f"Template not found: {template_name}")

        template = self._templates[template_name]
        return self._substitute_placeholders(template, placeholders)

    def _substitute_placeholders(self, template: str, placeholders: PromptPlaceholders) -> str:
        """Substitute all placeholders in a template."""
        result = template
        result = result.replace('{class_name}', placeholders.class_name)
        result = result.replace('{module_name}', placeholders.module_name)
        result = result.replace('{import_statement}', placeholders.import_statement)
        result = result.replace('{context_code}', placeholders.context_code)
        result = result.replace('{context_level}', placeholders.context_level)
        result = result.replace('{helper_types}', placeholders.helper_types)
        result = result.replace('{public_methods_list}', placeholders.public_methods_list)
        return result

    def get_simple_prompt(self, placeholders: PromptPlaceholders) -> str:
        """
        Generate a prompt for SimplePrompting strategy.

        Args:
            placeholders: Values to substitute into the template

        Returns:
            Complete prompt string
        """
        return self.render_template('simple', placeholders)

    def get_cot_prompts(self, placeholders: PromptPlaceholders) -> Dict[str, str]:
        """
        Generate prompts for ChainOfThought strategy.

        Args:
            placeholders: Values to substitute into templates

        Returns:
            Dictionary with keys 'step1', 'step2', 'step3'
        """
        return {
            'step1': self.render_template('cot_step1', placeholders),
            'step2': self.render_template('cot_step2', placeholders),
            'step3': self.render_template('cot_step3', placeholders),
        }

    def get_cot_combined(self, placeholders: PromptPlaceholders) -> str:
        """
        Generate combined CoT prompt (all steps in one file).

        This matches the format used by existing prompt.txt files.

        Args:
            placeholders: Values to substitute into templates

        Returns:
            Combined prompt with 1), 2), 3) sections
        """
        steps = self.get_cot_prompts(placeholders)
        return COT_COMBINED_TEMPLATE.format(
            step1=steps['step1'],
            step2=steps['step2'],
            step3=steps['step3']
        )

    @staticmethod
    def get_context_level_description(context_type: str) -> str:
        """
        Get human-readable description for a context level.

        Args:
            context_type: One of 'interface', 'interface_docstring', 'full_context'

        Returns:
            Human-readable description
        """
        descriptions = {
            'interface': 'interface (method signatures only)',
            'interface_docstring': 'interface with docstrings',
            'full_context': 'full class implementation',
        }
        return descriptions.get(context_type, context_type)


def create_placeholders_from_extractor(extractor, context_type: str) -> PromptPlaceholders:
    """
    Create PromptPlaceholders from a ClassContextExtractor.

    This is a convenience function that bridges the extractor and template manager.

    Args:
        extractor: ClassContextExtractor instance
        context_type: One of 'interface', 'interface_docstring', 'full_context'

    Returns:
        PromptPlaceholders ready for template substitution
    """
    info = extractor.get_class_info()

    helper_types_desc = ""
    if info.helper_types:
        helper_types_desc = f"Helper types: {', '.join(info.helper_types)}"

    return PromptPlaceholders(
        class_name=info.name,
        module_name=info.module_name,
        import_statement=info.import_statement,
        context_code=extractor.extract_context(context_type),
        context_level=PromptTemplateManager.get_context_level_description(context_type),
        helper_types=helper_types_desc,
        public_methods_list=', '.join(info.public_methods)
    )


def main():
    """CLI for testing the template manager."""
    import argparse
    from class_context_extractor import ClassContextExtractor

    parser = argparse.ArgumentParser(description='Generate prompts from templates')
    parser.add_argument('source_file', help='Path to Python source file')
    parser.add_argument('--class-name', help='Name of class (auto-detected if single)')
    parser.add_argument('--strategy', choices=['simple', 'cot'], default='simple',
                        help='Prompting strategy')
    parser.add_argument('--context', choices=['interface', 'interface_docstring', 'full_context'],
                        default='full_context', help='Context level')

    args = parser.parse_args()

    try:
        extractor = ClassContextExtractor(Path(args.source_file), args.class_name)
        placeholders = create_placeholders_from_extractor(extractor, args.context)

        manager = PromptTemplateManager()

        if args.strategy == 'simple':
            prompt = manager.get_simple_prompt(placeholders)
            print(prompt)
        else:
            prompt = manager.get_cot_combined(placeholders)
            print(prompt)

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
