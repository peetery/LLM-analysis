"""
Mutation Testing Backfill Script.

This script enables running mutation testing on Windows-generated test results
by executing it in WSL/Linux where fork support is available. It identifies
result directories without valid mutation results and runs mutmut analysis.

The script:
    - Verifies execution on Linux/WSL (required for fork support)
    - Locates the mutants directory in the repository
    - VALIDATES existing results (killed > 0 OR survived > 0 means valid)
    - Re-runs mutation testing for invalid results
    - Parses results and updates analysis files
    - Generates updated summary reports

Usage:
    # From WSL (not Windows):
    cd /mnt/c/Users/.../LLM-analysis/automation

    # Process all experiments, skipping those with valid results
    python3 run_mutmut_backfill.py --results-dir cli_results

    # Only fix experiments with invalid results (no_test_results, no_mutants)
    python3 run_mutmut_backfill.py --results-dir cli_results --fix-invalid

    # Force re-run for all experiments
    python3 run_mutmut_backfill.py --results-dir cli_results --force

    # Process specific run
    python3 run_mutmut_backfill.py --results-dir cli_results --run-id 001
"""

import sys
import os
import json
import subprocess
import logging
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Tuple

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_platform():
    """
    Verify that the script is running on Linux/WSL.

    Mutation testing requires fork() support which is not available on Windows.
    This function ensures the script is executed in an appropriate environment.

    Raises:
        SystemExit: If running on Windows
    """
    import platform
    if platform.system() == 'Windows':
        logger.error(
            "This script must be run in WSL/Linux "
            "(mutation testing requires fork support)"
        )
        logger.error(
            "Open WSL and run: "
            "cd /mnt/c/Users/.../automation && python3 run_mutmut_backfill.py"
        )
        sys.exit(1)
    logger.info("Running on Linux/WSL")


def find_mutants_directory() -> Optional[Path]:
    """
    Locate the mutants directory in parent directories.

    Searches up to 3 levels above the current directory for the mutants
    directory containing mutation testing configuration.

    Returns:
        Path to mutants directory if found, None otherwise
    """
    current_dir = Path(".")

    for i in range(3):
        check_dir = current_dir / ("../" * i) / "mutants"
        if check_dir.exists():
            return check_dir.resolve()

    logger.error("Mutants directory not found")
    return None


def check_existing_results(experiment_dir: Path) -> Tuple[bool, str]:
    """
    Check if experiment has valid mutation results.

    Returns:
        (is_valid, reason)
        - (True, "valid") if results exist and are valid (killed > 0 OR survived > 0)
        - (False, reason) if results are missing or invalid
    """
    analysis_file = experiment_dir / "analysis_results.json"
    mutmut_results_file = experiment_dir / "mutmut_results.txt"

    # Check if files exist
    if not analysis_file.exists():
        return False, "no_analysis_file"

    if not mutmut_results_file.exists():
        return False, "no_results_file"

    if mutmut_results_file.stat().st_size == 0:
        return False, "empty_results_file"

    # Check analysis_results.json for valid mutation data
    try:
        with open(analysis_file, 'r') as f:
            analysis = json.load(f)

        mutation = analysis.get('mutation') or {}
        total_mutants = mutation.get('total_mutants', 0)
        killed = mutation.get('killed', 0)
        survived = mutation.get('survived', 0)

        # Valid if: has mutants AND (killed > 0 OR survived > 0)
        if total_mutants > 0 and (killed > 0 or survived > 0):
            return True, "valid"
        elif total_mutants == 0:
            return False, "no_mutants"
        else:
            return False, "no_test_results"  # Has mutants but killed=0 AND survived=0

    except (json.JSONDecodeError, Exception) as e:
        return False, f"json_error: {e}"


def run_mutmut_for_experiment(experiment_dir: Path, mutants_dir: Path, force: bool = False):
    logger.info(f"\n{'='*60}")
    try:
        rel_path = experiment_dir.relative_to(Path.cwd())
        logger.info(f"Processing: {rel_path}")
    except ValueError:
        logger.info(f"Processing: {experiment_dir}")
    logger.info(f"{'='*60}")

    test_file = experiment_dir / "mutmut_test.py"
    if not test_file.exists():
        logger.warning(f"No mutmut_test.py found - skipping")
        return False

    # Define mutmut_results_file path
    mutmut_results_file = experiment_dir / "mutmut_results.txt"

    # Check if valid results already exist
    if not force:
        is_valid, reason = check_existing_results(experiment_dir)
        if is_valid:
            logger.info(f"Valid mutation results exist - skipping")
            return False
        elif reason in ["no_test_results", "no_mutants"]:
            logger.info(f"Invalid results found ({reason}) - will re-run mutmut")
            # Delete invalid results so we re-run
            if mutmut_results_file.exists():
                mutmut_results_file.unlink()
                logger.info(f"Deleted invalid results file")
        else:
            logger.info(f"No valid results ({reason}) - will run mutmut")

    try:
        test_content = test_file.read_text()  # mutmut_test.py is already filtered by experiment_runner

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
        logger.info(f"Copied test to {test_dst} (fixed imports for src-layout)")

        logger.info("Cleaning mutmut cache and temp files...")
        # Remove .mutmut-cache files
        for cache_file in mutants_dir.glob(".mutmut-cache*"):
            try:
                cache_file.unlink()
            except:
                pass

        # Remove meta files
        for meta_file in mutants_dir.rglob("*.meta"):
            try:
                meta_file.unlink()
            except:
                pass

        # Remove pyproject.toml (conflicts with setup.cfg in mutmut 3.x)
        pyproject_file = mutants_dir / "pyproject.toml"
        if pyproject_file.exists():
            try:
                pyproject_file.unlink()
                logger.info("Removed pyproject.toml (conflicts with setup.cfg)")
            except:
                pass

        # Remove .coverage file
        coverage_file = mutants_dir / ".coverage"
        if coverage_file.exists():
            try:
                coverage_file.unlink()
            except:
                pass

        # Remove mutants directory (mutmut output cache)
        mutants_output_dir = mutants_dir / "mutants"
        if mutants_output_dir.exists():
            try:
                shutil.rmtree(mutants_output_dir)
            except:
                pass

        logger.info("Running mutmut... (this may take 5-10 minutes)")
        run_result = subprocess.run(
            ['mutmut', 'run'], env={**os.environ, 'PATH': os.environ.get('PATH', '') + ':' + str(Path.home() / '.local' / 'bin')},
            cwd=mutants_dir,
            capture_output=True,
            text=True,
            timeout=600
        )

        logger.debug(f"   Mutmut stdout: {run_result.stdout[:500]}")
        logger.debug(f"   Mutmut stderr: {run_result.stderr[:500]}")

        if run_result.returncode != 0:
            logger.warning(f"Mutmut run returned code {run_result.returncode}")

        results_result = subprocess.run(
            ['mutmut', 'results'], env={**os.environ, 'PATH': os.environ.get('PATH', '') + ':' + str(Path.home() / '.local' / 'bin')},
            cwd=mutants_dir,
            capture_output=True,
            text=True
        )

        mutmut_results_file.write_text(results_result.stdout)
        logger.info(f"Saved mutation results to {mutmut_results_file}")

        combined_output = run_result.stdout + "\n" + run_result.stderr
        stats = parse_mutmut_results(combined_output)

        if stats['killed'] == 0 and stats['survived'] == 0 and stats['total_mutants'] > 0:
            logger.warning("Failed to parse stats from mutmut run output, trying mutmut results...")
            stats_alt = parse_mutmut_results_from_text(results_result.stdout)
            if stats_alt['killed'] > 0 or stats_alt['survived'] > 0:
                logger.info("Successfully parsed from mutmut results output")
                stats = stats_alt
            else:
                logger.warning("Could not parse mutation stats - results may be incomplete")
        stats_file = experiment_dir / "mutmut-stats.json"
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        logger.info(f"Saved stats: {stats}")

        update_analysis_results(experiment_dir, stats)

        regenerate_markdown_summary(experiment_dir)

        logger.info(f"Mutation testing completed successfully!")
        logger.info(f"   Mutation score: {stats['mutation_score']}%")
        logger.info(f"   Killed: {stats['killed']}/{stats['total_mutants']}")

        return True

    except subprocess.TimeoutExpired:
        logger.error(f"Mutation testing timed out after 10 minutes")
        return False
    except Exception as e:
        logger.error(f"Error running mutation testing: {e}")
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
        logger.warning(f"analysis_results.json not found - skipping update")
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

    logger.info(f"Updated {analysis_file}")


def regenerate_markdown_summary(experiment_dir: Path):
    analysis_file = experiment_dir / "analysis_results.json"
    experiment_file = experiment_dir / "experiment_results.json"

    if not analysis_file.exists() or not experiment_file.exists():
        logger.warning("Missing JSON files - skipping markdown regeneration")
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
    logger.info(f"Regenerated {md_file}")


def process_results_directory(results_dir: Path, run_id_filter: str = None, force: bool = False, fix_invalid: bool = False):
    check_platform()

    mutants_dir = find_mutants_directory()
    if not mutants_dir:
        logger.error("Cannot proceed without mutants directory")
        sys.exit(1)

    logger.info(f"Using mutants directory: {mutants_dir}")

    if run_id_filter:
        logger.info(f"Filtering for run ID: run_{run_id_filter}")

    if fix_invalid:
        logger.info(f"Fix-invalid mode: only processing experiments with invalid results")

    if force:
        logger.info(f"Force mode: will re-run mutmut even for valid results")

    experiment_dirs = []
    for test_file in results_dir.rglob("mutmut_test.py"):
        exp_dir = test_file.parent

        if run_id_filter:
            if f"run_{run_id_filter}" not in str(exp_dir):
                continue

        # If fix_invalid mode, only include experiments with invalid results
        if fix_invalid:
            is_valid, reason = check_existing_results(exp_dir)
            if is_valid:
                continue  # Skip valid experiments
            if reason not in ["no_test_results", "no_mutants", "no_results_file", "empty_results_file"]:
                continue  # Skip experiments with other issues (like no analysis file)

        experiment_dirs.append(exp_dir)

    if not experiment_dirs:
        if run_id_filter:
            logger.warning(f"No experiments found in {results_dir} for run_{run_id_filter}")
        else:
            logger.warning(f"No experiments found in {results_dir}")
        return

    logger.info(f"Found {len(experiment_dirs)} experiments to process")

    processed_count = 0
    skipped_count = 0
    failed_count = 0

    for exp_dir in experiment_dirs:
        success = run_mutmut_for_experiment(exp_dir, mutants_dir, force=force)
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
    parser.add_argument('--force', action='store_true',
                        help='Re-run mutmut even for experiments with valid results')
    parser.add_argument('--fix-invalid', action='store_true',
                        help='Only process experiments with invalid results (no_test_results, no_mutants)')

    args = parser.parse_args()

    if args.experiment_dir:
        check_platform()
        mutants_dir = find_mutants_directory()
        if not mutants_dir:
            logger.error("Cannot proceed without mutants directory")
            sys.exit(1)

        exp_dir = Path(args.experiment_dir).resolve()
        if not exp_dir.exists():
            logger.error(f"Experiment directory not found: {exp_dir}")
            sys.exit(1)

        run_mutmut_for_experiment(exp_dir, mutants_dir, force=args.force)
    else:
        results_dir = Path(args.results_dir)
        if not results_dir.exists():
            logger.error(f"Results directory not found: {results_dir}")
            sys.exit(1)

        process_results_directory(results_dir, run_id_filter=args.run_id, force=args.force, fix_invalid=args.fix_invalid)


if __name__ == "__main__":
    main()
