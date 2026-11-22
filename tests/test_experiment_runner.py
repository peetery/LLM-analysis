import json
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from automation.experiment_runner import ExperimentRunner


class TestEfficientAnalysis(unittest.TestCase):
    def test_coverage_counts_wholly_missing_branches(self):
        runner = ExperimentRunner()
        report = {
            'files': {
                'order_calculator.py': {
                    'summary': {
                        'num_statements': 10, 'covered_lines': 6, 'missing_lines': 4,
                        'num_branches': 8, 'covered_branches': 3, 'num_partial_branches': 1
                    },
                    'missing_lines': [6, 7, 8, 9],
                    'missing_branches': [[6, 7], [6, 8]]
                }
            }
        }
        coverage = runner.parse_coverage_json(report)
        self.assertEqual(coverage['coverage_percent'], 60.0)
        self.assertEqual(coverage['branch_coverage_percent'], 37.5)
        self.assertEqual(coverage['missing_branches'], [[6, 7], [6, 8]])

    def test_efficient_pipeline_runs_suite_once_and_preserves_failures(self):
        for fails in (False, True):
            with self.subTest(fails=fails), TemporaryDirectory() as directory:
                root = Path(directory)
                shutil.copy2(Path(__file__).parents[1] / 'order_calculator.py', root)
                tests = root / 'tests.py'
                tests.write_text(
                    'import unittest\nfrom order_calculator import OrderCalculator\n'
                    'class Tests(unittest.TestCase):\n'
                    '    def test_default(self):\n'
                    '        with open("executions.txt", "a") as output:\n'
                    '            output.write("run\\n")\n'
                    f'        self.assertEqual(OrderCalculator().tax_rate, {0 if fails else 0.23})\n'
                )
                runner = ExperimentRunner(efficient_analysis=True)
                data = {
                    'test_file': str(tests), 'model': 'fixture',
                    'strategy': 'simple_prompting', 'context_type': 'full_context',
                    'timestamp': 'fixture', 'response_time': 0
                }
                with patch.object(runner, 'run_mutation_testing', return_value={}) as mutation:
                    result = runner.run_analysis(root, data)
                self.assertEqual((root / 'executions.txt').read_text(), 'run\n')
                self.assertEqual(result['compilation']['execution_success'], not fails)
                self.assertEqual(mutation.call_count, 0 if fails else 1)
                self.assertFalse((root / 'htmlcov').exists())
                self.assertTrue((root / 'coverage.json').exists())
                self.assertEqual(
                    json.loads((root / 'analysis_results.json').read_text())['compilation'],
                    result['compilation']
                )

    def test_empty_or_invalid_suites_never_receive_mutation_scores(self):
        for code in ('import unittest\n', 'def broken(:\n'):
            with self.subTest(code=code), TemporaryDirectory() as directory:
                root = Path(directory)
                shutil.copy2(Path(__file__).parents[1] / 'order_calculator.py', root)
                tests = root / 'tests.py'
                tests.write_text(code)
                data = {
                    'test_file': str(tests), 'model': 'fixture',
                    'strategy': 'simple_prompting', 'context_type': 'full_context',
                    'timestamp': 'fixture', 'response_time': 0
                }
                runner = ExperimentRunner(efficient_analysis=True)
                with patch.object(runner, 'run_mutation_testing') as mutation:
                    report = runner.run_analysis(root, data)
                mutation.assert_not_called()
                self.assertIsNone(report['mutation'])
                self.assertNotIn('mutation_score', report['summary'])


if __name__ == '__main__':
    unittest.main()
