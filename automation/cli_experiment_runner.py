"""
CLI Experiment Runner.

This module orchestrates automated unit test generation experiments using
CLI-based LLM tools. It manages experiment execution, result storage, and
analysis pipeline integration for evaluating different prompting strategies
and code context levels across multiple models.

The runner supports:
    - Single experiment execution
    - Batch experiment processing from configuration files
    - Multi-run experiment tracking (run_001, run_002, etc.)
    - Integration with analysis pipeline (coverage, mutation testing)
    - Universal mode: Test generation for any Python class
    - Legacy mode: Backwards compatible with OrderCalculator

Usage:
    # Legacy mode (OrderCalculator)
    python cli_experiment_runner.py --model MODEL --strategy STRATEGY --context CONTEXT

    # Universal mode (any class)
    python cli_experiment_runner.py --source-file path/to/class.py --model MODEL --strategy STRATEGY --context CONTEXT

    python cli_experiment_runner.py --config config.json
    python cli_experiment_runner.py --list-models
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

from cli_automation import (
    ClaudeCodeClient,
    GeminiCLIClient
)

from experiment_runner import ExperimentRunner
from prompt_strategies import SimplePrompting, ChainOfThoughtPrompting

logger = logging.getLogger(__name__)


class CLIExperimentRunner:
    """
    Orchestrates CLI-based LLM experiments for test generation.

    Supports two modes:
    - Legacy mode (extractor=None): Uses OrderCalculator defaults
    - Universal mode (extractor provided): Uses any Python class
    """

    def __init__(self, base_results_dir="cli_results", run_id=None, extractor=None):
        """
        Initialize the CLI experiment runner.

        Args:
            base_results_dir: Directory for storing results
            run_id: Run identifier (number, "overwrite", or None for auto-increment)
            extractor: ClassContextExtractor for universal mode (None for legacy)
        """
        self.base_results_dir = Path(base_results_dir)
        self.base_results_dir.mkdir(parents=True, exist_ok=True)
        self.run_id = run_id
        self.extractor = extractor

        self.cli_clients = {
            # Claude Code models (newest first)
            'claude-code-opus-4.5': lambda: ClaudeCodeClient(model="claude-opus-4.5"),
            'claude-code-sonnet-4.5': lambda: ClaudeCodeClient(model="claude-sonnet-4.5"),
            'claude-code-opus-4.1': lambda: ClaudeCodeClient(model="claude-opus-4.1"),

            # Gemini CLI models (newest first)
            'gemini-3-pro': lambda: GeminiCLIClient(model="gemini-3-pro-preview"),
            'gemini-3-flash': lambda: GeminiCLIClient(model="gemini-3-flash-preview"),
            'gemini-2.5-pro': lambda: GeminiCLIClient(model="gemini-2.5-pro"),
            'gemini-2.5-flash': lambda: GeminiCLIClient(model="gemini-2.5-flash"),
        }

        logger.info(f"CLI Experiment Runner initialized with {len(self.cli_clients)} models")
        if run_id == "overwrite":
            logger.info("Run mode: overwrite (legacy - no run numbering)")
        elif run_id is not None:
            logger.info(f"Run mode: fixed run ID = {run_id}")
        else:
            logger.info("Run mode: auto-increment run numbering")

    def _get_next_run_id(self, base_dir: Path) -> int:
        if not base_dir.exists():
            return 1

        existing_runs = []
        for item in base_dir.iterdir():
            if item.is_dir() and item.name.startswith('run_'):
                try:
                    run_num = int(item.name.replace('run_', ''))
                    existing_runs.append(run_num)
                except ValueError:
                    continue

        if not existing_runs:
            return 1

        return max(existing_runs) + 1

    def _get_result_dir(self, strategy_name: str, context_type: str, model_name: str) -> Path:
        base_path = self.base_results_dir / strategy_name / context_type / model_name

        if self.run_id == "overwrite":
            return base_path

        if self.run_id is None:
            next_run = self._get_next_run_id(base_path)
            run_dir = base_path / f"run_{next_run:03d}"
            logger.info(f"Using auto-incremented run: run_{next_run:03d}")
            return run_dir

        run_dir = base_path / f"run_{self.run_id:03d}"
        logger.info(f"Using specified run: run_{self.run_id:03d}")
        return run_dir

    def run_single_experiment(
        self,
        model_name: str,
        strategy_name: str,
        context_type: str
    ) -> dict:
        logger.info(f"Starting CLI experiment: {model_name} - {strategy_name} - {context_type}")

        if model_name not in self.cli_clients:
            raise ValueError(
                f"Unknown model: {model_name}. "
                f"Available models: {', '.join(self.cli_clients.keys())}"
            )

        result_dir = self._get_result_dir(strategy_name, context_type, model_name)
        result_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Results will be saved to: {result_dir}")

        try:
            client_factory = self.cli_clients[model_name]

            with client_factory() as client:
                logger.info(f"Initialized client: {client}")

                # Create strategy with extractor for universal mode
                if strategy_name == "simple_prompting":
                    strategy = SimplePrompting(extractor=self.extractor)
                elif strategy_name == "chain_of_thought_prompting":
                    strategy = ChainOfThoughtPrompting(extractor=self.extractor)
                else:
                    raise ValueError(f"Unknown strategy: {strategy_name}")

                logger.info(f"Executing {strategy_name} strategy...")
                strategy_result = strategy.execute(client, context_type)

                if not strategy_result:
                    logger.error("Strategy execution failed")
                    return None

                # Create analysis runner with extractor for universal mode
                analysis_runner = ExperimentRunner(extractor=self.extractor)

                experiment_data = analysis_runner.save_experiment_results(
                    result_dir,
                    strategy_result,
                    model_name,
                    strategy_name,
                    context_type
                )

                if not experiment_data:
                    logger.error("Failed to save experiment results")
                    return None

                logger.info("Running analysis pipeline...")
                analysis_results = analysis_runner.run_analysis(result_dir, experiment_data)

                logger.info("Experiment completed successfully")
                logger.info("Results saved to: %s", result_dir)

                return {
                    'experiment': experiment_data,
                    'analysis': analysis_results,
                    'result_dir': str(result_dir)
                }

        except Exception as e:
            logger.error(f"Experiment failed: {e}", exc_info=True)
            return None

    def run_batch_experiments(self, config_file: str) -> list:
        logger.info(f"Running batch experiments from: {config_file}")

        with open(config_file) as f:
            config = json.load(f)

        experiments = config['experiments']
        delay = config.get('delay_between_experiments', 10)

        results = []

        for i, experiment in enumerate(experiments):
            model = experiment['model']
            strategy = experiment['strategy']
            context = experiment['context']

            logger.info(f"\n{'='*60}")
            logger.info(f"Experiment {i+1}/{len(experiments)}")
            logger.info(f"Model: {model}")
            logger.info(f"Strategy: {strategy}")
            logger.info(f"Context: {context}")
            logger.info(f"{'='*60}\n")

            result = self.run_single_experiment(model, strategy, context)

            if result:
                results.append(result)
                logger.info("Experiment %d/%d completed successfully", i+1, len(experiments))
            else:
                logger.error("Experiment %d/%d failed", i+1, len(experiments))

            if i < len(experiments) - 1:
                import time
                logger.info("Waiting %ds before next experiment...", delay)
                time.sleep(delay)

        logger.info("="*60)
        logger.info("Batch completed: %d/%d experiments successful", len(results), len(experiments))
        logger.info("="*60)

        return results

    def get_available_models(self) -> list:
        return list(self.cli_clients.keys())

    def print_available_models(self):
        print("\nAvailable CLI Models:")
        print("="*60)

        groups = {
            'OpenAI Codex': [k for k in self.cli_clients if k.startswith('codex-')],
            'Claude Code': [k for k in self.cli_clients if k.startswith('claude-code-')],
            'GitHub Copilot': [k for k in self.cli_clients if k.startswith('copilot-')],
            'Google Gemini': [k for k in self.cli_clients if k.startswith('gemini-')],
        }

        for tool, models in groups.items():
            print(f"\n{tool}:")
            for model in models:
                print(f"  - {model}")

        print("\n" + "="*60)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='CLI Experiment Runner with multi-run support',
        epilog='''
Run ID modes:
  - No --run-id: Auto-increment (creates run_001, run_002, etc.)
  - --run-id N: Use specific run number (e.g., --run-id 1 creates run_001)
  - --run-id overwrite: Legacy mode, no run numbering (overwrites existing results)

Source file modes:
  - No --source-file: Legacy mode (OrderCalculator)
  - --source-file path/to/class.py: Universal mode (any Python class)
  - --source-file path/to/class.py --class-name ClassName: Specify class if multiple

Examples:
  # Legacy mode - OrderCalculator (creates run_001)
  python cli_experiment_runner.py --model claude-code-sonnet-4.5 --strategy simple_prompting --context interface

  # Universal mode - any class
  python cli_experiment_runner.py --source-file my_module.py --model claude-code-sonnet-4.5 --strategy simple_prompting --context full_context

  # Universal mode with specific class name
  python cli_experiment_runner.py --source-file my_module.py --class-name MyClass --model claude-code-sonnet-4.5 --strategy simple_prompting --context interface

  # Batch with auto-increment
  python cli_experiment_runner.py --config cli_config.json
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--model', help='Model name')
    parser.add_argument('--strategy', choices=['simple_prompting', 'chain_of_thought_prompting'],
                        help='Prompting strategy')
    parser.add_argument('--context', choices=['interface', 'interface_docstring', 'full_context'],
                        help='Code context level')
    parser.add_argument('--config', help='JSON config file for batch experiments')
    parser.add_argument('--list-models', action='store_true',
                        help='List available models')
    parser.add_argument('--run-id', type=str, default=None,
                        help='Run identifier: number (e.g., 1), "overwrite", or omit for auto-increment')
    parser.add_argument('--results-dir', type=str, default='cli_results',
                        help='Directory for storing results (default: cli_results)')

    # Universal mode arguments
    parser.add_argument('--source-file', type=str, default=None,
                        help='Path to Python source file (universal mode). If omitted, uses legacy OrderCalculator mode.')
    parser.add_argument('--class-name', type=str, default=None,
                        help='Name of the class to test (auto-detected if single class in file)')
    parser.add_argument('--legacy', action='store_true',
                        help='Force legacy mode even if --source-file is provided')

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('cli_automation.log'),
            logging.StreamHandler()
        ]
    )

    run_id = None
    if args.run_id is not None:
        if args.run_id.lower() == 'overwrite':
            run_id = "overwrite"
        else:
            try:
                run_id = int(args.run_id)
                if run_id < 1:
                    print("Error: --run-id must be positive integer or 'overwrite'")
                    return
            except ValueError:
                print(f"Error: Invalid --run-id '{args.run_id}'. Use integer or 'overwrite'")
                return

    # Create extractor for universal mode
    extractor = None
    if args.source_file and not args.legacy:
        try:
            from class_context_extractor import ClassContextExtractor
            source_path = Path(args.source_file)
            if not source_path.exists():
                print(f"Error: Source file not found: {args.source_file}")
                return
            extractor = ClassContextExtractor(source_path, args.class_name)
            info = extractor.get_class_info()
            print(f"\n{'='*60}")
            print(f"Universal mode: {info.name}")
            print(f"Module: {info.module_name}")
            print(f"Methods: {len(info.public_methods)}")
            print(f"Helper types: {', '.join(info.helper_types) or 'None'}")
            print(f"{'='*60}\n")
        except Exception as e:
            print(f"Error initializing class extractor: {e}")
            return
    else:
        print("\n" + "="*60)
        print("Legacy mode: OrderCalculator")
        print("="*60 + "\n")

    runner = CLIExperimentRunner(
        base_results_dir=args.results_dir,
        run_id=run_id,
        extractor=extractor
    )

    if args.list_models:
        runner.print_available_models()
        return

    if args.config:
        results = runner.run_batch_experiments(args.config)

        batch_results_file = Path("cli_batch_results.json")
        with open(batch_results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        logger.info(f"Batch results saved to: {batch_results_file}")

    elif args.model and args.strategy and args.context:
        result = runner.run_single_experiment(
            args.model,
            args.strategy,
            args.context
        )

        if result:
            print("\n" + "="*60)
            print("Experiment completed successfully")
            print(f"Results saved to: {result['result_dir']}")
            print("="*60 + "\n")
        else:
            print("\n" + "="*60)
            print("Experiment failed")
            print("="*60 + "\n")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
