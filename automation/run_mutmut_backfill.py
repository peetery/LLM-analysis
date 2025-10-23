import sys
import json
import subprocess
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def check_platform():
    import platform
    if platform.system() == 'Windows':
        logger.error("❌ This script must be run in WSL/Linux (mutation testing requires fork support)")
        logger.error("💡 Open WSL and run: cd /mnt/c/Users/.../automation && python3 run_mutmut_backfill.py")
        sys.exit(1)
    logger.info("✅ Running on Linux/WSL")


def find_mutants_directory():
    current_dir = Path(".")

    for i in range(3):
        check_dir = current_dir / ("../" * i) / "mutants"
        if check_dir.exists():
            return check_dir.resolve()

    logger.error("❌ Mutants directory not found")
    return None


def filter_passing_tests(test_file: Path) -> str:
    import ast
    import re

    try:
        logger.info("🔍 Filtering tests - identifying passing tests...")

        result = subprocess.run(
            ['python3', '-m', 'unittest', test_file.stem, '-v'],
            cwd=test_file.parent,
            capture_output=True,
            text=True,
            timeout=120
        )

        passing_tests = set()
        failing_tests = set()

        for line in result.stderr.split('\n'):
            if ' ... ok' in line:
                match = re.search(r'(test_\w+)', line)
                if match:
                    passing_tests.add(match.group(1))
            elif ' ... FAIL' in line or ' ... ERROR' in line:
                match = re.search(r'(test_\w+)', line)
                if match:
                    failing_tests.add(match.group(1))

        logger.info(f"📊 Test filtering: {len(passing_tests)} passing, {len(failing_tests)} failing")

        if not passing_tests:
            logger.warning("⚠️  No passing tests found - using original file")
            return test_file.read_text()

        if not failing_tests:
            logger.info("✅ All tests pass - no filtering needed")
            return test_file.read_text()

        test_content = test_file.read_text()
        tree = ast.parse(test_content)

        filtered_tree = ast.parse("")

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                new_class = ast.ClassDef(
                    name=node.name,
                    bases=node.bases,
                    keywords=node.keywords,
                    body=[],
                    decorator_list=node.decorator_list
                )

                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        if (item.name in ['setUp', 'tearDown'] or
                            item.name in passing_tests):
                            new_class.body.append(item)
                    else:
                        new_class.body.append(item)

                if any(isinstance(item, ast.FunctionDef) and item.name.startswith('test_')
                       for item in new_class.body):
                    filtered_tree.body.append(new_class)
            else:
                filtered_tree.body.append(node)

        try:
            filtered_content = ast.unparse(filtered_tree)
            logger.info(f"✅ Filtered out {len(failing_tests)} failing tests")
            return filtered_content
        except AttributeError:
            logger.warning("⚠️  ast.unparse not available - using line-based filtering")
            return filter_tests_line_based(test_content, failing_tests)

    except Exception as e:
        logger.error(f"⚠️  Test filtering failed: {e} - using original file")
        return test_file.read_text()


def filter_tests_line_based(test_content: str, failing_tests: set) -> str:
    lines = test_content.split('\n')
    filtered_lines = []
    skip_until_next_method = False
    current_indent = 0

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('def test_'):
            method_name = stripped.split('(')[0].replace('def ', '')

            if method_name in failing_tests:
                skip_until_next_method = True
                current_indent = len(line) - len(line.lstrip())
                continue
            else:
                skip_until_next_method = False
                filtered_lines.append(line)
        elif skip_until_next_method:
            line_indent = len(line) - len(line.lstrip())
            if line.strip() and line_indent <= current_indent:
                skip_until_next_method = False
                filtered_lines.append(line)
        else:
            filtered_lines.append(line)

    return '\n'.join(filtered_lines)


def run_mutmut_for_experiment(experiment_dir: Path, mutants_dir: Path):
    logger.info(f"\n{'='*60}")
    try:
        rel_path = experiment_dir.relative_to(Path.cwd())
        logger.info(f"Processing: {rel_path}")
    except ValueError:
        logger.info(f"Processing: {experiment_dir}")
    logger.info(f"{'='*60}")

    test_file = experiment_dir / "mutmut_test.py"
    if not test_file.exists():
        logger.warning(f"⚠️  No mutmut_test.py found - skipping")
        return False

    mutmut_results_file = experiment_dir / "mutmut_results.txt"
    if mutmut_results_file.exists() and mutmut_results_file.stat().st_size > 0:
        logger.info(f"ℹ️  Mutation results already exist - skipping")
        return False

    try:
        test_content = filter_passing_tests(test_file)

        if 'from order_calculator import' in test_content or 'import order_calculator' in test_content:
            import_fix = """import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

"""
            lines = test_content.split('\n')
            fixed_lines = []
            import_added = False

            for line in lines:
                if not import_added and ('from order_calculator' in line or 'import order_calculator' in line):
                    fixed_lines.append(import_fix.rstrip())
                    import_added = True
                fixed_lines.append(line)

            test_content = '\n'.join(fixed_lines)

        test_dst = mutants_dir / "tests" / "mutmut_test.py"
        test_dst.parent.mkdir(exist_ok=True)
        test_dst.write_text(test_content)
        logger.info(f"✓ Wrote filtered test to {test_dst} (fixed imports for src-layout)")

        logger.info("Cleaning mutmut cache...")
        for cache_file in mutants_dir.glob(".mutmut-cache*"):
            cache_file.unlink()

        for meta_file in mutants_dir.rglob("*.meta"):
            meta_file.unlink()

        logger.info("Running mutmut... (this may take 5-10 minutes)")
        run_result = subprocess.run(
            ['mutmut', 'run'],
            cwd=mutants_dir,
            capture_output=True,
            text=True,
            timeout=600
        )

        logger.debug(f"   Mutmut stdout: {run_result.stdout[:500]}")
        logger.debug(f"   Mutmut stderr: {run_result.stderr[:500]}")

        if run_result.returncode != 0:
            logger.warning(f"⚠️  Mutmut run returned code {run_result.returncode}")

        results_result = subprocess.run(
            ['mutmut', 'results'],
            cwd=mutants_dir,
            capture_output=True,
            text=True
        )

        mutmut_results_file.write_text(results_result.stdout)
        logger.info(f"✓ Saved mutation results to {mutmut_results_file}")

        combined_output = run_result.stdout + "\n" + run_result.stderr
        stats = parse_mutmut_results(combined_output)

        if stats['killed'] == 0 and stats['survived'] == 0 and stats['total_mutants'] > 0:
            logger.warning("⚠️  Failed to parse stats from mutmut run output, trying mutmut results...")
            stats_alt = parse_mutmut_results_from_text(results_result.stdout)
            if stats_alt['killed'] > 0 or stats_alt['survived'] > 0:
                logger.info("✅ Successfully parsed from mutmut results output")
                stats = stats_alt
            else:
                logger.warning("⚠️  Could not parse mutation stats - results may be incomplete")
        stats_file = experiment_dir / "mutmut-stats.json"
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        logger.info(f"✓ Saved stats: {stats}")

        update_analysis_results(experiment_dir, stats)

        regenerate_markdown_summary(experiment_dir)

        logger.info(f"✅ Mutation testing completed successfully!")
        logger.info(f"   Mutation score: {stats['mutation_score']}%")
        logger.info(f"   Killed: {stats['killed']}/{stats['total_mutants']}")

        return True

    except subprocess.TimeoutExpired:
        logger.error(f"❌ Mutation testing timed out after 10 minutes")
        return False
    except Exception as e:
        logger.error(f"❌ Error running mutation testing: {e}")
        return False


def parse_mutmut_results_from_text(mutmut_output: str) -> dict:
    import re

    stats = {
        'total_mutants': 0,
        'killed': 0,
        'survived': 0,
        'timeout': 0,
        'suspicious': 0,
        'skipped': 0,
        'mutation_score': 0.0
    }

    killed_match = re.search(r'Killed mutants \((\d+)/(\d+)\):', mutmut_output)
    if killed_match:
        stats['killed'] = int(killed_match.group(1))
        stats['total_mutants'] = int(killed_match.group(2))

    survived_match = re.search(r'Survived mutants \((\d+)/(\d+)\):', mutmut_output)
    if survived_match:
        stats['survived'] = int(survived_match.group(1))
        if stats['total_mutants'] == 0:
            stats['total_mutants'] = int(survived_match.group(2))

    suspicious_match = re.search(r'Suspicious mutants \((\d+)/(\d+)\):', mutmut_output)
    if suspicious_match:
        stats['suspicious'] = int(suspicious_match.group(1))

    timeout_match = re.search(r'Timeout mutants \((\d+)/(\d+)\):', mutmut_output)
    if timeout_match:
        stats['timeout'] = int(timeout_match.group(1))

    if stats['killed'] == 0 and stats['survived'] == 0:
        for line in mutmut_output.split('\n'):
            if ': killed' in line:
                stats['killed'] += 1
            elif ': survived' in line:
                stats['survived'] += 1
            elif ': timeout' in line:
                stats['timeout'] += 1
            elif ': suspicious' in line:
                stats['suspicious'] += 1
            elif ': skipped' in line:
                stats['skipped'] += 1

        stats['total_mutants'] = (stats['killed'] + stats['survived'] +
                                 stats['timeout'] + stats['suspicious'] + stats['skipped'])

    if stats['total_mutants'] > 0:
        stats['mutation_score'] = round((stats['killed'] / stats['total_mutants']) * 100, 1)

    return stats


def parse_mutmut_results(mutmut_output: str) -> dict:
    import re

    stats = {
        'total_mutants': 0,
        'killed': 0,
        'survived': 0,
        'timeout': 0,
        'suspicious': 0,
        'skipped': 0,
        'mutation_score': 0.0
    }

    # Look for emoji pattern, allowing any character before the numbers
    # Pattern explanation:
    # .*? - any characters (spinner)
    # (\d+)/(\d+) - progress like "205/205"
    # \s+ - whitespace
    # 🎉\s+(\d+) - killed count
    # 🫥\s+(\d+) - (unknown, usually 0)
    # ⏰\s+(\d+) - timeout
    # 🤔\s+(\d+) - suspicious
    # 🙁\s+(\d+) - survived
    # 🔇\s+(\d+) - skipped
    emoji_pattern = r'(\d+)/(\d+)\s+🎉\s+(\d+)\s+🫥\s+(\d+)\s+⏰\s+(\d+)\s+🤔\s+(\d+)\s+🙁\s+(\d+)\s+🔇\s+(\d+)'

    all_matches = list(re.finditer(emoji_pattern, mutmut_output))

    if all_matches:
        final_match = None
        for match in reversed(all_matches):
            progress = int(match.group(1))
            total = int(match.group(2))
            if progress == total:
                final_match = match
                break

        if not final_match:
            final_match = all_matches[-1]

        if final_match:
            progress_total = int(final_match.group(2))
            killed = int(final_match.group(3))
            timeout = int(final_match.group(5))
            suspicious = int(final_match.group(6))
            survived = int(final_match.group(7))
            skipped = int(final_match.group(8))

            stats.update({
                'total_mutants': progress_total,
                'killed': killed,
                'survived': survived,
                'timeout': timeout,
                'suspicious': suspicious,
                'skipped': skipped
            })

            if progress_total > 0:
                stats['mutation_score'] = round((killed / progress_total) * 100, 1)

    return stats


def update_analysis_results(experiment_dir: Path, mutmut_stats: dict):
    analysis_file = experiment_dir / "analysis_results.json"

    if not analysis_file.exists():
        logger.warning(f"⚠️  analysis_results.json not found - skipping update")
        return

    with open(analysis_file, 'r') as f:
        analysis = json.load(f)

    analysis['mutation'] = mutmut_stats

    if 'summary' in analysis:
        analysis['summary']['mutation_score'] = mutmut_stats.get('mutation_score', 0)
        analysis['summary']['mutants_killed'] = mutmut_stats.get('killed', 0)
        analysis['summary']['mutants_survived'] = mutmut_stats.get('survived', 0)
        analysis['summary']['total_mutants'] = mutmut_stats.get('total_mutants', 0)

    with open(analysis_file, 'w') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    logger.info(f"✓ Updated {analysis_file}")


def regenerate_markdown_summary(experiment_dir: Path):
    analysis_file = experiment_dir / "analysis_results.json"
    experiment_file = experiment_dir / "experiment_results.json"

    if not analysis_file.exists() or not experiment_file.exists():
        logger.warning("⚠️  Missing JSON files - skipping markdown regeneration")
        return

    with open(analysis_file, 'r') as f:
        analysis = json.load(f)

    with open(experiment_file, 'r') as f:
        experiment = json.load(f)

    summary = analysis.get('summary', {})
    model_name = experiment['model']
    strategy = experiment['strategy']
    context = experiment['context_type']

    md_file = experiment_dir / f"podsumowanie-{model_name.replace('.', '').replace(' ', '-')}.md"

    content = f"""# Podsumowanie analizy pokrycia testów jednostkowych (Model: {model_name})
# Kontekst: {context}
# Strategia promptowania: {strategy.replace('_', '-')}

## coverage.py
- missing: {summary.get('missing_statements', 'N/A')}
- coverage: {summary.get('statement_coverage', 'N/A')}%

## mutmut.py
⠋ {summary.get('total_mutants', 0)}/{summary.get('total_mutants', 0)}  🎉 {summary.get('mutants_killed', 0)} 🫥 0  ⏰ 0  🤔 0  🙁 {summary.get('mutants_survived', 0)}  🔇 0

## Rezultaty
- Compilation success rate: {summary.get('compilation_success_rate', 0)}%
- Statement coverage: {summary.get('statement_coverage', 0)}%
- Branch coverage: {summary.get('branch_coverage', 0)}%
- Mutation score: {summary.get('mutation_score', 0)}%

## Test Quality Metrics (Objective)

### Test Execution
- Tests generated: {summary.get('total_test_methods', 0)}
- Tests passed: {summary.get('tests_passed', 0)}
- Tests failed: {summary.get('tests_failed', 0)}
- Test success rate: {summary.get('test_success_rate', 0)}%

### Method Coverage
- OrderCalculator methods tested: {summary.get('methods_tested_count', 0)}/{summary.get('total_methods', 12)}
- Method coverage rate: {summary.get('method_coverage_rate', 0)}%

### Test Structure
- Total assertions: {summary.get('total_assertions', 0)}
- Average assertions per test: {summary.get('avg_assertions_per_test', 0)}
- Tests with multiple assertions: {summary.get('tests_with_multiple_assertions', 0)}
- Tests with error handling: {summary.get('tests_with_error_handling', 0)}
- Has setUp/tearDown: {'Yes' if summary.get('has_setup_teardown', False) else 'No'}
- Average test length (LOC): {summary.get('average_test_length', 0)}

### Code Quality
- Potential duplicate tests found: {summary.get('duplicate_tests_found', 0)}

## Advanced Quality Analysis

### Assertion Quality
- Assertion quality score: {summary.get('assertion_quality_score', 0)}%
- Strong assertions: {summary.get('strong_assertions_count', 0)}
- Weak assertions: {summary.get('weak_assertions_count', 0)}

### Exception Testing Quality
- Exception quality score: {summary.get('exception_quality_score', 0)}%
- Exception tests: {summary.get('exception_tests_count', 0)}
- Tests checking exception messages: {summary.get('tests_with_message_check', 0)}

### Test Independence
- Independence score: {summary.get('independence_score', 100)}%
- Tests are independent: {'Yes' if summary.get('is_independent', True) else 'No'}

### Naming Quality
- Naming quality score: {summary.get('naming_quality_score', 0)}%
- Average test name length: {summary.get('average_name_length', 0)} characters

### Code Smells
- Code smell score: {summary.get('smell_score', 100)}% (100 = no smells)
- Total code smells found: {summary.get('total_smells_found', 0)}

## Overall Quality Score
**{summary.get('overall_quality_score', 0)}%** (weighted average of all quality metrics)

## Automatycznie wygenerowane przez LLM Testing Automation
- Response time: {summary.get('response_time', 0):.2f}s
- Generated at: {summary.get('timestamp', 'N/A')}
- Mutation testing updated: {datetime.now().isoformat()}

"""

    md_file.write_text(content, encoding='utf-8')
    logger.info(f"✓ Regenerated {md_file}")


def process_results_directory(results_dir: Path, run_id_filter: str = None):
    check_platform()

    mutants_dir = find_mutants_directory()
    if not mutants_dir:
        logger.error("❌ Cannot proceed without mutants directory")
        sys.exit(1)

    logger.info(f"Using mutants directory: {mutants_dir}")

    if run_id_filter:
        logger.info(f"Filtering for run ID: run_{run_id_filter}")

    experiment_dirs = []
    for test_file in results_dir.rglob("mutmut_test.py"):
        exp_dir = test_file.parent

        if run_id_filter:
            if f"run_{run_id_filter}" not in str(exp_dir):
                continue

        experiment_dirs.append(exp_dir)

    if not experiment_dirs:
        if run_id_filter:
            logger.warning(f"⚠️  No experiments found in {results_dir} for run_{run_id_filter}")
        else:
            logger.warning(f"⚠️  No experiments found in {results_dir}")
        return

    logger.info(f"Found {len(experiment_dirs)} experiments to process")

    processed_count = 0
    skipped_count = 0
    failed_count = 0

    for exp_dir in experiment_dirs:
        success = run_mutmut_for_experiment(exp_dir, mutants_dir)
        if success:
            processed_count += 1
        elif success is False:
            skipped_count += 1
        else:
            failed_count += 1

    logger.info(f"\n{'='*60}")
    logger.info(f"Backfill Summary:")
    logger.info(f"  Processed: {processed_count}")
    logger.info(f"  Skipped: {skipped_count}")
    logger.info(f"  Failed: {failed_count}")
    logger.info(f"{'='*60}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Add mutmut results to existing experiments (supports multi-run structure)',
        epilog='''
Examples:
  # Process all experiments in cli_results
  python3 run_mutmut_backfill.py --results-dir cli_results

  # Process only run_001 experiments
  python3 run_mutmut_backfill.py --results-dir cli_results --run-id 001

  # Process only run_002 and run_003
  python3 run_mutmut_backfill.py --results-dir cli_results --run-id 002
  python3 run_mutmut_backfill.py --results-dir cli_results --run-id 003

  # Process single experiment directory
  python3 run_mutmut_backfill.py --experiment-dir cli_results/simple_prompting/interface/claude-code-sonnet-4.5/run_001
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--results-dir', default='cli_results',
                        help='Results directory to process (default: cli_results)')
    parser.add_argument('--experiment-dir',
                        help='Process single experiment directory')
    parser.add_argument('--run-id', type=str, default=None,
                        help='Filter by run ID (e.g., "001" for run_001, "002" for run_002)')

    args = parser.parse_args()

    if args.experiment_dir:
        check_platform()
        mutants_dir = find_mutants_directory()
        if not mutants_dir:
            logger.error("❌ Cannot proceed without mutants directory")
            sys.exit(1)

        exp_dir = Path(args.experiment_dir).resolve()
        if not exp_dir.exists():
            logger.error(f"❌ Experiment directory not found: {exp_dir}")
            sys.exit(1)

        run_mutmut_for_experiment(exp_dir, mutants_dir)
    else:
        results_dir = Path(args.results_dir)
        if not results_dir.exists():
            logger.error(f"❌ Results directory not found: {results_dir}")
            sys.exit(1)

        process_results_directory(results_dir, run_id_filter=args.run_id)


if __name__ == "__main__":
    main()
