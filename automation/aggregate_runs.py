
import json
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any
from statistics import mean, stdev
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def find_run_directories(experiment_path: Path) -> List[Path]:
    if not experiment_path.exists():
        return []

    run_dirs = []
    for item in experiment_path.iterdir():
        if item.is_dir() and item.name.startswith('run_'):
            try:
                run_num = int(item.name.replace('run_', ''))
                run_dirs.append((run_num, item))
            except ValueError:
                continue

    run_dirs.sort(key=lambda x: x[0])
    return [path for _, path in run_dirs]


def load_analysis_results(run_dir: Path) -> Dict[str, Any]:
    analysis_file = run_dir / "analysis_results.json"
    if not analysis_file.exists():
        return None

    try:
        with open(analysis_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load {analysis_file}: {e}")
        return None


def extract_metrics(analysis: Dict[str, Any]) -> Dict[str, float]:
    if not analysis:
        return {}

    summary = analysis.get('summary', {})

    metrics = {
        'statement_coverage': summary.get('statement_coverage', 0),
        'branch_coverage': summary.get('branch_coverage', 0),
        'missing_statements': summary.get('missing_statements', 0),

        'mutation_score': summary.get('mutation_score', 0),
        'mutants_killed': summary.get('mutants_killed', 0),
        'mutants_survived': summary.get('mutants_survived', 0),
        'total_mutants': summary.get('total_mutants', 0),

        'compilation_success': 1 if summary.get('compilation_success_rate', 0) == 100 else 0,
        'tests_passed': summary.get('tests_passed', 0),
        'tests_failed': summary.get('tests_failed', 0),
        'test_success_rate': summary.get('test_success_rate', 0),
        'total_test_methods': summary.get('total_test_methods', 0),

        'total_assertions': summary.get('total_assertions', 0),
        'avg_assertions_per_test': summary.get('avg_assertions_per_test', 0),
        'tests_with_error_handling': summary.get('tests_with_error_handling', 0),
        'average_test_length': summary.get('average_test_length', 0),

        'assertion_quality_score': summary.get('assertion_quality_score', 0),
        'exception_quality_score': summary.get('exception_quality_score', 0),
        'independence_score': summary.get('independence_score', 100),
        'naming_quality_score': summary.get('naming_quality_score', 0),
        'smell_score': summary.get('smell_score', 100),
        'overall_quality_score': summary.get('overall_quality_score', 0),

        'response_time': summary.get('response_time', 0),

        'method_coverage_rate': summary.get('method_coverage_rate', 0),
        'methods_tested_count': summary.get('methods_tested_count', 0),
    }

    return metrics


def compute_statistics(values: List[float]) -> Dict[str, float]:
    if not values:
        return {
            'mean': 0,
            'std': 0,
            'min': 0,
            'max': 0,
            'count': 0
        }

    values = [v for v in values if v is not None]

    if not values:
        return {
            'mean': 0,
            'std': 0,
            'min': 0,
            'max': 0,
            'count': 0
        }

    return {
        'mean': round(mean(values), 2),
        'std': round(stdev(values), 2) if len(values) > 1 else 0,
        'min': round(min(values), 2),
        'max': round(max(values), 2),
        'count': len(values)
    }


def aggregate_experiment_runs(experiment_path: Path) -> Dict[str, Any]:
    logger.info(f"Aggregating runs for: {experiment_path}")

    run_dirs = find_run_directories(experiment_path)

    if not run_dirs:
        logger.warning(f"No run directories found in {experiment_path}")
        return None

    logger.info(f"Found {len(run_dirs)} runs: {[r.name for r in run_dirs]}")

    all_metrics = []
    run_details = []

    for run_dir in run_dirs:
        analysis = load_analysis_results(run_dir)
        if analysis:
            metrics = extract_metrics(analysis)
            all_metrics.append(metrics)
            run_details.append({
                'run': run_dir.name,
                'metrics': metrics
            })
        else:
            logger.warning(f"Could not load analysis from {run_dir.name}")

    if not all_metrics:
        logger.error(f"No valid analysis results found in any run")
        return None

    aggregated = {
        'experiment_path': str(experiment_path.relative_to(Path.cwd())),
        'total_runs': len(run_dirs),
        'valid_runs': len(all_metrics),
        'run_details': run_details,
        'statistics': {}
    }

    metric_names = set()
    for metrics in all_metrics:
        metric_names.update(metrics.keys())

    for metric_name in sorted(metric_names):
        values = [m.get(metric_name, 0) for m in all_metrics]
        aggregated['statistics'][metric_name] = compute_statistics(values)

    logger.info(f"✅ Aggregated {len(all_metrics)} runs successfully")

    return aggregated


def generate_markdown_report(aggregated_data: List[Dict[str, Any]], output_file: Path):
    lines = [
        "# Multi-Run Aggregated Results",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"Total experiments analyzed: {len(aggregated_data)}",
        ""
    ]

    for exp_data in aggregated_data:
        exp_path = exp_data['experiment_path']
        stats = exp_data['statistics']

        lines.extend([
            f"## {exp_path}",
            "",
            f"**Runs**: {exp_data['valid_runs']}/{exp_data['total_runs']}",
            "",
            "### Key Metrics",
            ""
        ])

        lines.extend([
            "#### Coverage",
            "",
            f"- **Statement Coverage**: {stats['statement_coverage']['mean']:.1f}% "
            f"(σ={stats['statement_coverage']['std']:.1f}, "
            f"min={stats['statement_coverage']['min']:.1f}, "
            f"max={stats['statement_coverage']['max']:.1f})",
            "",
            f"- **Branch Coverage**: {stats['branch_coverage']['mean']:.1f}% "
            f"(σ={stats['branch_coverage']['std']:.1f}, "
            f"min={stats['branch_coverage']['min']:.1f}, "
            f"max={stats['branch_coverage']['max']:.1f})",
            ""
        ])

        lines.extend([
            "#### Mutation Testing",
            "",
            f"- **Mutation Score**: {stats['mutation_score']['mean']:.1f}% "
            f"(σ={stats['mutation_score']['std']:.1f}, "
            f"min={stats['mutation_score']['min']:.1f}, "
            f"max={stats['mutation_score']['max']:.1f})",
            "",
            f"- **Mutants Killed**: {stats['mutants_killed']['mean']:.1f} "
            f"(σ={stats['mutants_killed']['std']:.1f})",
            ""
        ])

        lines.extend([
            "#### Test Quality",
            "",
            f"- **Test Success Rate**: {stats['test_success_rate']['mean']:.1f}% "
            f"(σ={stats['test_success_rate']['std']:.1f})",
            "",
            f"- **Total Tests**: {stats['total_test_methods']['mean']:.1f} "
            f"(σ={stats['total_test_methods']['std']:.1f})",
            "",
            f"- **Overall Quality Score**: {stats['overall_quality_score']['mean']:.1f}% "
            f"(σ={stats['overall_quality_score']['std']:.1f})",
            ""
        ])

        cv_mutation = (stats['mutation_score']['std'] / stats['mutation_score']['mean'] * 100) if stats['mutation_score']['mean'] > 0 else 0
        cv_coverage = (stats['statement_coverage']['std'] / stats['statement_coverage']['mean'] * 100) if stats['statement_coverage']['mean'] > 0 else 0

        stability = "High" if cv_mutation < 5 and cv_coverage < 5 else "Medium" if cv_mutation < 10 and cv_coverage < 10 else "Low"

        lines.extend([
            "#### Stability Assessment",
            "",
            f"- **Mutation Score CV**: {cv_mutation:.2f}%",
            f"- **Coverage CV**: {cv_coverage:.2f}%",
            f"- **Overall Stability**: {stability}",
            "",
            "---",
            ""
        ])

    output_file.write_text('\n'.join(lines), encoding='utf-8')
    logger.info(f"✅ Markdown report saved to: {output_file}")


def process_results_directory(results_dir: Path) -> List[Dict[str, Any]]:
    logger.info(f"Processing results directory: {results_dir}")

    experiment_dirs = set()

    for run_dir in results_dir.rglob("run_*"):
        if run_dir.is_dir():
            experiment_dirs.add(run_dir.parent)

    if not experiment_dirs:
        logger.warning(f"No experiments with runs found in {results_dir}")
        return []

    logger.info(f"Found {len(experiment_dirs)} experiments with multiple runs")

    aggregated_results = []
    for exp_dir in sorted(experiment_dirs):
        result = aggregate_experiment_runs(exp_dir)
        if result:
            aggregated_results.append(result)

    return aggregated_results


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Aggregate results from multiple experiment runs',
        epilog='''
Examples:
  # Aggregate single experiment
  python aggregate_runs.py --experiment-path cli_results/simple_prompting/interface/claude-code-sonnet-4.5

  # Aggregate all experiments in directory
  python aggregate_runs.py --results-dir cli_results

  # Save results to custom file
  python aggregate_runs.py --results-dir cli_results --output my_results.json --markdown my_report.md
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--experiment-path', type=str,
                        help='Path to single experiment directory (containing run_XXX subdirs)')
    parser.add_argument('--results-dir', type=str, default='cli_results',
                        help='Process all experiments in results directory (default: cli_results)')
    parser.add_argument('--output', type=str, default='aggregated_results.json',
                        help='Output JSON file (default: aggregated_results.json)')
    parser.add_argument('--markdown', type=str, default='aggregated_report.md',
                        help='Output markdown report (default: aggregated_report.md)')

    args = parser.parse_args()

    aggregated_results = []

    if args.experiment_path:
        exp_path = Path(args.experiment_path)
        if not exp_path.exists():
            logger.error(f"Experiment path not found: {exp_path}")
            sys.exit(1)

        result = aggregate_experiment_runs(exp_path)
        if result:
            aggregated_results.append(result)
    else:
        results_dir = Path(args.results_dir)
        if not results_dir.exists():
            logger.error(f"Results directory not found: {results_dir}")
            sys.exit(1)

        aggregated_results = process_results_directory(results_dir)

    if not aggregated_results:
        logger.error("No aggregated results to save")
        sys.exit(1)

    output_file = Path(args.output)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(aggregated_results, f, indent=2, ensure_ascii=False)

    logger.info(f"✅ Aggregated results saved to: {output_file}")

    markdown_file = Path(args.markdown)
    generate_markdown_report(aggregated_results, markdown_file)

    print("\n" + "="*60)
    print("Aggregation Summary")
    print("="*60)
    print(f"Experiments processed: {len(aggregated_results)}")
    print(f"JSON output: {output_file}")
    print(f"Markdown report: {markdown_file}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
