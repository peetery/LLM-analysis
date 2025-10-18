"""
CLI Experiment Runner
"""

import logging
import json
from pathlib import Path

from cli_automation import (
    ClaudeCodeClient
)

from experiment_runner import ExperimentRunner
from prompt_strategies import SimplePrompting, ChainOfThoughtPrompting

logger = logging.getLogger(__name__)


class CLIExperimentRunner:

    def __init__(self, base_results_dir="cli_results"):
        self.base_results_dir = Path(base_results_dir)
        self.base_results_dir.mkdir(parents=True, exist_ok=True)

        self.cli_clients = {
            'claude-code-sonnet-4.5': lambda: ClaudeCodeClient(model="claude-sonnet-4.5"),
        }

        logger.info(f"CLI Experiment Runner initialized with {len(self.cli_clients)} models")

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

        result_dir = self.base_results_dir / strategy_name / context_type / model_name
        result_dir.mkdir(parents=True, exist_ok=True)

        try:
            client_factory = self.cli_clients[model_name]

            with client_factory() as client:
                logger.info(f"Initialized client: {client}")

                if strategy_name == "simple_prompting":
                    strategy = SimplePrompting()
                elif strategy_name == "chain_of_thought_prompting":
                    strategy = ChainOfThoughtPrompting()
                else:
                    raise ValueError(f"Unknown strategy: {strategy_name}")

                logger.info(f"Executing {strategy_name} strategy...")
                strategy_result = strategy.execute(client, context_type)

                if not strategy_result:
                    logger.error("Strategy execution failed")
                    return None

                web_runner = ExperimentRunner()

                experiment_data = web_runner.save_experiment_results(
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
                analysis_results = web_runner.run_analysis(result_dir, experiment_data)

                logger.info(f"✅ Experiment completed successfully!")
                logger.info(f"Results saved to: {result_dir}")

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
                logger.info(f"✅ Experiment {i+1} completed successfully")
            else:
                logger.error(f"❌ Experiment {i+1} failed")

            if i < len(experiments) - 1:
                import time
                logger.info(f"⏳ Waiting {delay}s before next experiment...")
                time.sleep(delay)

        logger.info(f"\n{'='*60}")
        logger.info(f"Batch completed!")
        logger.info(f"Successful: {len(results)}/{len(experiments)}")
        logger.info(f"{'='*60}\n")

        return results

    def get_available_models(self) -> list:
        return list(self.cli_clients.keys())

    def print_available_models(self):
        print("\n📋 Available CLI Models:")
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

    parser = argparse.ArgumentParser(description='CLI Experiment Runner')
    parser.add_argument('--model', help='Model name')
    parser.add_argument('--strategy', choices=['simple_prompting', 'chain_of_thought_prompting'],
                        help='Prompting strategy')
    parser.add_argument('--context', choices=['interface', 'interface_docstring', 'full_context'],
                        help='Code context level')
    parser.add_argument('--config', help='JSON config file for batch experiments')
    parser.add_argument('--list-models', action='store_true',
                        help='List available models')

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('cli_automation.log'),
            logging.StreamHandler()
        ]
    )

    runner = CLIExperimentRunner()

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
            print("\n✅ Experiment completed successfully!")
            print(f"Results saved to: {result['result_dir']}")
        else:
            print("\n❌ Experiment failed!")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
