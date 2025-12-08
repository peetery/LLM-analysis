import json
import subprocess
import logging
import re
import ast
from pathlib import Path
from datetime import datetime
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExperimentRunner:

    def __init__(self, base_results_dir="prompts_results"):
        self.base_results_dir = Path(base_results_dir)
        self.current_experiment = None
    
    def save_experiment_results(self, result_dir, strategy_result, model_name, strategy_name, context_type):
        timestamp = datetime.now().isoformat()

        if strategy_name == "simple_prompting":
            test_code = self.extract_test_code(strategy_result['response'])
            response_time = strategy_result['response_time']
        else:  # chain_of_thought_prompting
            response_text = strategy_result.get('final_response') or strategy_result.get('response', '')
            test_code = self.extract_test_code(response_text)
            response_time = strategy_result.get('total_response_time', 0)
        
        if not test_code:
            logger.error("Failed to extract test code from response")
            return None
        
        tests_file = result_dir / "tests.py"
        tests_file.write_text(test_code)

        source_file = Path("../order_calculator.py")
        if not source_file.exists():
            source_file = Path("../../order_calculator.py")
        if not source_file.exists():
            source_file = Path("order_calculator.py")

        if source_file.exists():
            dest_file = result_dir / "order_calculator.py"
            shutil.copy2(source_file, dest_file)
            logger.info(f"✓ Copied {source_file} to test directory")
        else:
            logger.error("✗ order_calculator.py not found - tests will fail")

        mutmut_test_file = result_dir / "mutmut_test.py"
        self.create_filtered_test_file(tests_file, mutmut_test_file)
        
        experiment_data = {
            'model': model_name,
            'strategy': strategy_name,
            'context_type': context_type,
            'timestamp': timestamp,
            'response_time': response_time,
            'test_file': str(tests_file),
            'raw_results': strategy_result
        }
        
        results_file = result_dir / "experiment_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(experiment_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to {result_dir}")
        return experiment_data

    def create_filtered_test_file(self, source_test_file, target_test_file):
        try:
            result = subprocess.run(
                ['python', '-m', 'unittest', source_test_file.stem, '-v'],
                cwd=source_test_file.parent,
                capture_output=True,
                text=True,
                timeout=120
            )

            passing_tests = set()
            failing_tests = set()
            current_test = None

            for line in result.stderr.split('\n'):
                # Check if this line contains a test name (format: test_xxx (module.class.test_xxx))
                test_name_match = re.search(r'^(test_\w+)\s+\(', line)
                if test_name_match:
                    current_test = test_name_match.group(1)

                # Check for test result on this line or use current_test from previous line
                if ' ... ok' in line:
                    # Try to find test name on same line first (no docstring case)
                    match = re.search(r'(test_\w+)', line)
                    if match:
                        passing_tests.add(match.group(1))
                    elif current_test:
                        passing_tests.add(current_test)
                        current_test = None
                elif ' ... FAIL' in line or ' ... ERROR' in line:
                    match = re.search(r'(test_\w+)', line)
                    if match:
                        failing_tests.add(match.group(1))
                    elif current_test:
                        failing_tests.add(current_test)
                        current_test = None

            logger.info(f"📊 Test filtering: {len(passing_tests)} passing, {len(failing_tests)} failing")

            if not passing_tests:
                logger.warning("⚠️  No passing tests found - copying original file for mutmut")
                shutil.copy2(source_test_file, target_test_file)
                return

            test_content = source_test_file.read_text()
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
                filtered_code = ast.unparse(filtered_tree)
            except AttributeError:
                logger.warning("⚠️  ast.unparse not available - using line-based filtering")
                filtered_code = self._filter_tests_line_based(test_content, failing_tests)

            target_test_file.write_text(filtered_code)
            logger.info(f"✅ Created filtered test file: {target_test_file}")
            logger.info(f"   Removed {len(failing_tests)} failing tests for mutation testing")

        except Exception as e:
            logger.error(f"Test filtering failed: {e} - copying original file")
            shutil.copy2(source_test_file, target_test_file)

    def _filter_tests_line_based(self, test_content, failing_tests):
        lines = test_content.split('\n')
        filtered_lines = []
        skip_until_next_method = False
        current_indent = 0

        for i, line in enumerate(lines):
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

    def extract_test_code(self, response_text):
        logger.info(f"Extracting test code from response ({len(response_text)} chars)")
        logger.debug(f"First 300 chars: {response_text[:300]}")

        def clean_code_block(code):
            lines = code.split('\n')
            cleaned_lines = []

            for line in lines:
                original_line = line
                line_stripped = line.strip()

                ui_artifacts = [
                    'python', 'kopiuj', 'edytuj', 'copy', 'edit', 'skopiuj',
                    'bash', 'shell', 'powershell', 'cmd', 'javascript', 'js',
                    'html', 'css', 'sql', 'json', 'xml', 'yaml'
                ]

                if line_stripped.lower() in ui_artifacts:
                    continue

                if line_stripped.startswith('```'):
                    continue

                if not cleaned_lines and not line_stripped:
                    continue

                cleaned_lines.append(original_line)

            while cleaned_lines and not cleaned_lines[-1].strip():
                cleaned_lines.pop()

            return '\n'.join(cleaned_lines)

        code_blocks = re.findall(r'```python\n(.*?)\n```', response_text, re.DOTALL)
        if not code_blocks:
            code_blocks = re.findall(r'```\n(.*?)\n```', response_text, re.DOTALL)

        if code_blocks:
            logger.info(f"✓ Found {len(code_blocks)} code blocks")

            for i, block in enumerate(code_blocks):
                cleaned_block = clean_code_block(block)
                smart_result = self._extract_tests_smart(cleaned_block)

                if smart_result:
                    logger.info(f"✓ Smart extraction successful from block {i+1}")
                    logger.info(f"✓ Extracted {len(smart_result)} chars of test code")
                    return smart_result

            for block in code_blocks:
                cleaned_block = clean_code_block(block)
                if 'unittest' in cleaned_block or 'def test' in cleaned_block:
                    logger.warning("⚠️ Smart extraction failed, using fallback")
                    return self._ensure_imports(cleaned_block)

            logger.warning("⚠️ No unittest found, using first block")
            return self._ensure_imports(clean_code_block(code_blocks[0]))

        logger.warning("No markdown code blocks found, trying fallback extraction...")
        lines = response_text.split('\n')
        code_start = None

        for i, line in enumerate(lines):
            line_stripped = line.strip()
            if (line_stripped.startswith('import ') or
                line_stripped.startswith('from ') or
                (line_stripped.startswith('class ') and 'Test' in line_stripped)):
                code_start = i
                break

        if code_start is not None:
            logger.info(f"✓ Found code start at line {code_start} (fallback method)")
            code_lines = lines[code_start:]
            code = '\n'.join(code_lines)
            extracted = clean_code_block(code)
            logger.info(f"✓ Extracted {len(extracted)} chars of test code (fallback)")
            return self._ensure_imports(extracted)

        logger.error("✗ Failed to extract any test code from response")
        return None

    def _extract_tests_smart(self, code_text):
        try:
            tree = ast.parse(code_text)
        except SyntaxError:
            logger.debug("Code is not valid Python, skipping smart extraction")
            return None

        imports = []
        test_classes = []
        has_ordercalculator_import = False

        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append(node)
                if isinstance(node, ast.ImportFrom):
                    if node.module == 'order_calculator':
                        for alias in node.names:
                            if alias.name == 'OrderCalculator':
                                has_ordercalculator_import = True
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name == 'order_calculator':
                            has_ordercalculator_import = True

            elif isinstance(node, ast.ClassDef):
                if node.name.startswith('Test'):
                    test_classes.append(node)
                    logger.debug(f"Found test class: {node.name}")
                elif node.name in ['OrderCalculator', 'Item']:
                    logger.debug(f"Skipping implementation class: {node.name}")
                else:
                    test_classes.append(node)

        if not test_classes:
            logger.debug("No test classes found in this block")
            return None

        new_tree = ast.Module(body=imports + test_classes, type_ignores=[])

        try:
            code = ast.unparse(new_tree)
        except AttributeError:
            logger.warning("ast.unparse not available, using fallback")
            return None

        if not has_ordercalculator_import:
            logger.info("✓ Auto-adding missing OrderCalculator import")
            code = "from order_calculator import OrderCalculator, Item\n\n" + code

        return code

    def _ensure_imports(self, code_text):
        has_import = (
            re.search(r'from\s+order_calculator\s+import.*OrderCalculator', code_text) or
            re.search(r'import\s+order_calculator', code_text)
        )

        if not has_import:
            logger.info("✓ Auto-adding missing OrderCalculator import (fallback)")
            lines = code_text.split('\n')

            last_import_idx = -1
            for i, line in enumerate(lines):
                if line.strip().startswith(('import ', 'from ')):
                    last_import_idx = i

            if last_import_idx >= 0:
                lines.insert(last_import_idx + 1, 'from order_calculator import OrderCalculator, Item')
            else:
                lines.insert(0, 'from order_calculator import OrderCalculator, Item')
                lines.insert(1, '')

            code_text = '\n'.join(lines)

        return code_text
    
    def run_analysis(self, result_dir, experiment_data):
        tests_file = Path(experiment_data['test_file'])
        
        if not tests_file.exists():
            logger.error(f"Test file not found: {tests_file}")
            return None
        
        analysis_results = {}
        
        compilation_result = self.test_compilation_and_execution(tests_file)
        analysis_results['compilation'] = compilation_result
        
        if not compilation_result['compilation_success']:
            logger.error("Tests do not compile")

        if compilation_result['compilation_success']:
            coverage_results = self.run_coverage_analysis(result_dir, tests_file)
            analysis_results['coverage'] = coverage_results
        else:
            analysis_results['coverage'] = None
        
        if compilation_result['compilation_success']:
            mutation_results = self.run_mutation_testing(result_dir)
            analysis_results['mutation'] = mutation_results
        else:
            analysis_results['mutation'] = None
        
        scenario_analysis = self.analyze_test_scenarios(tests_file)
        analysis_results['scenarios'] = scenario_analysis
        
        summary = self.generate_comprehensive_summary(analysis_results, experiment_data)
        analysis_results['summary'] = summary
        
        self.save_analysis_results(result_dir, analysis_results, experiment_data)
        
        return analysis_results
    
    def test_compilation(self, tests_file):
        try:
            result = subprocess.run(
                ['python', '-m', 'py_compile', tests_file.name],
                cwd=tests_file.parent,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info("✓ Tests compile successfully")
                return True
            else:
                logger.error(f"✗ Compilation failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Compilation test failed: {e}")
            return False
    
    def run_coverage_analysis(self, result_dir, tests_file):
        try:
            cmd = [
                'python', '-m', 'coverage', 'run',
                '--source=.', '--branch', '-m', 'unittest',
                tests_file.stem
            ]

            result = subprocess.run(
                cmd,
                cwd=result_dir,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                logger.warning(f"⚠️  Some tests failed during coverage run, but continuing with coverage analysis")
                logger.debug(f"Test output: {result.stderr[:500]}")

            report_result = subprocess.run(
                ['python', '-m', 'coverage', 'report'],
                cwd=result_dir,
                capture_output=True,
                text=True
            )

            if report_result.returncode != 0:
                logger.error(f"Coverage report generation failed: {report_result.stderr}")
                return None

            subprocess.run(
                ['python', '-m', 'coverage', 'html'],
                cwd=result_dir,
                capture_output=True,
                text=True
            )

            coverage_data = self.parse_coverage_report(report_result.stdout)

            if coverage_data:
                logger.info(f"✓ Coverage: {coverage_data['coverage_percent']}% statement, {coverage_data['branch_coverage_percent']}% branch")

            return coverage_data

        except Exception as e:
            logger.error(f"Coverage analysis failed: {e}")
            return None
    
    def parse_coverage_report(self, coverage_output):
        lines = coverage_output.strip().split('\n')
        coverage_data = {
            'statements': 0,
            'missing': 0,
            'coverage_percent': 0,
            'branch_coverage_percent': 0,
            'partial_coverage': 0
        }

        for line in lines:
            if 'order_calculator.py' in line:
                parts = line.split()
                if len(parts) >= 6:
                    try:
                        coverage_data['statements'] = int(parts[1])
                        coverage_data['missing'] = int(parts[2])
                        coverage_data['coverage_percent'] = int(parts[5].replace('%', ''))

                        branch_total = int(parts[3])
                        branch_partial = int(parts[4])
                        if branch_total > 0:
                            branch_covered = branch_total - branch_partial
                            coverage_data['branch_coverage_percent'] = round((branch_covered / branch_total) * 100)

                    except (ValueError, IndexError) as e:
                        logger.warning(f"Failed to parse coverage line: {line}, error: {e}")
                        pass

        return coverage_data if coverage_data['statements'] > 0 else None
    
    def run_mutation_testing(self, result_dir):
        import platform

        if platform.system() == 'Windows':
            logger.warning("⚠️  Mutation testing requires Linux/WSL - skipping on Windows")
            logger.info("💡 Run 'python run_mutmut_backfill.py' in WSL to add mutation results later")
            return {
                'total_mutants': 0,
                'killed': 0,
                'survived': 0,
                'timeout': 0,
                'mutation_score': 0.0,
                'status': 'skipped_windows'
            }

        try:
            current_dir = Path(".")
            mutants_dir = None

            for i in range(3):
                check_dir = current_dir / ("../" * i) / "mutants"
                if check_dir.exists():
                    mutants_dir = check_dir.resolve()
                    break

            if not mutants_dir:
                logger.warning("Mutants directory not found - skipping mutation testing")
                return {
                    'total_mutants': 0,
                    'killed': 0,
                    'survived': 0,
                    'timeout': 0,
                    'mutation_score': 0.0,
                    'status': 'skipped_no_dir'
                }
            
            test_src = result_dir / "mutmut_test.py"
            test_dst = mutants_dir / "tests" / "mutmut_test.py"
            
            test_dst.parent.mkdir(exist_ok=True)
            shutil.copy2(test_src, test_dst)
            
            result = subprocess.run(
                ['python', '-m', 'mutmut', 'run'],
                cwd=mutants_dir,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            results_result = subprocess.run(
                ['python', '-m', 'mutmut', 'results'],
                cwd=mutants_dir,
                capture_output=True,
                text=True
            )
            
            mutmut_results_file = result_dir / "mutmut_results.txt"
            mutmut_results_file.write_text(results_result.stdout)
            
            stats = self.parse_mutmut_results(results_result.stdout)
            
            stats_file = result_dir / "mutmut-stats.json"
            with open(stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
            
            return stats
            
        except Exception as e:
            logger.error(f"Mutation testing failed: {e}")
            return None
    
    def parse_mutmut_results(self, mutmut_output):
        stats = {
            'total_mutants': 0,
            'killed': 0,
            'survived': 0,
            'timeout': 0,
            'suspicious': 0,
            'skipped': 0,
            'mutation_score': 0.0
        }
        
        emoji_pattern = r'(\d+)/(\d+)\s+🎉\s+(\d+)\s+🫥\s+(\d+)\s+⏰\s+(\d+)\s+🤔\s+(\d+)\s+🙁\s+(\d+)\s+🔇\s+(\d+)'
        match = re.search(emoji_pattern, mutmut_output)
        
        if match:
            progress_current = int(match.group(1))
            progress_total = int(match.group(2))
            killed = int(match.group(3))
            timeout = int(match.group(4))
            suspicious = int(match.group(6))
            survived = int(match.group(7))
            skipped = int(match.group(8))
            
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
        
        if stats['total_mutants'] == 0:
            for line in mutmut_output.split('\n'):
                if 'Total:' in line:
                    total_match = re.search(r'Total:\s*(\d+)', line)
                    if total_match:
                        stats['total_mutants'] = int(total_match.group(1))
                        
                if 'killed:' in line:
                    killed_match = re.search(r'killed:\s*(\d+)', line)
                    if killed_match:
                        stats['killed'] = int(killed_match.group(1))
                        
                if 'survived:' in line:
                    survived_match = re.search(r'survived:\s*(\d+)', line)
                    if survived_match:
                        stats['survived'] = int(survived_match.group(1))
        
        return stats
    
    def test_compilation_and_execution(self, tests_file):
        result = {
            'compilation_success': False,
            'execution_success': False,
            'tests_run': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'test_errors': [],
            'compilation_errors': []
        }
        
        try:
            compile_result = subprocess.run(
                ['python', '-m', 'py_compile', tests_file.name],
                cwd=tests_file.parent,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if compile_result.returncode == 0:
                result['compilation_success'] = True
                logger.info("✓ Tests compile successfully")
                
                unittest_result = subprocess.run(
                    ['python', '-m', 'unittest', tests_file.stem, '-v'],
                    cwd=tests_file.parent,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                self.parse_unittest_results(unittest_result.stderr, result)
                
            else:
                result['compilation_errors'] = [compile_result.stderr]
                logger.error(f"✗ Compilation failed: {compile_result.stderr}")
                
        except Exception as e:
            logger.error(f"Compilation/execution test failed: {e}")
            result['compilation_errors'] = [str(e)]
            
        return result
    
    def parse_unittest_results(self, unittest_output, result):
        lines = unittest_output.strip().split('\n')
        
        for line in lines:
            if 'Ran' in line and 'test' in line:
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        result['tests_run'] = int(parts[1])
                    except ValueError:
                        pass
            elif line.startswith('OK'):
                result['execution_success'] = True
                result['tests_passed'] = result['tests_run']
                result['tests_failed'] = 0
            elif 'FAILED' in line:
                result['execution_success'] = False
                # Przykład: "FAILED (failures=3, errors=2)"
                failures = self.extract_number_from_text(line, 'failures=')
                errors = self.extract_number_from_text(line, 'errors=')
                result['tests_failed'] = failures + errors
                result['tests_passed'] = result['tests_run'] - result['tests_failed']
                
    def extract_number_from_text(self, text, prefix):
        try:
            start = text.find(prefix)
            if start == -1:
                return 0
            start += len(prefix)
            end = start
            while end < len(text) and text[end].isdigit():
                end += 1
            return int(text[start:end]) if end > start else 0
        except:
            return 0
    
    def analyze_test_scenarios(self, tests_file):
        test_content = tests_file.read_text()
        test_methods = test_content.count('def test_')
        quality_metrics = self.analyze_test_quality(test_content)
        tested_methods = self.detect_tested_methods(test_content)
        duplicates = self.detect_duplicate_tests(tests_file)
        assertion_quality = self.analyze_assertion_quality(tests_file)
        exception_quality = self.analyze_exception_testing_quality(tests_file)
        independence = self.analyze_test_independence(tests_file)
        naming_quality = self.analyze_test_naming_quality(tests_file)
        code_smells = self.detect_code_smells(tests_file)

        return {
            'total_test_methods': test_methods,
            'quality_metrics': quality_metrics,
            'tested_methods': tested_methods,
            'duplicates': duplicates,
            'assertion_quality': assertion_quality,
            'exception_quality': exception_quality,
            'independence': independence,
            'naming_quality': naming_quality,
            'code_smells': code_smells
        }
    
    def detect_tested_methods(self, test_content):
        known_methods = [
            '__init__', 'add_item', 'remove_item', 'get_subtotal',
            'apply_discount', 'calculate_shipping', 'calculate_tax',
            'calculate_total', 'total_items', 'list_items',
            'is_empty', 'clear_order'
        ]

        tested_methods = {}
        for method in known_methods:
            if method == '__init__':
                pattern = r'OrderCalculator\s*\('
            else:
                pattern = rf'\.{method}\s*\('

            count = len(re.findall(pattern, test_content))
            if count > 0:
                tested_methods[method] = count

        return {
            'methods_tested': list(tested_methods.keys()),
            'methods_tested_count': len(tested_methods),
            'total_methods': len(known_methods),
            'method_coverage_rate': round((len(tested_methods) / len(known_methods)) * 100, 1),
            'method_call_counts': tested_methods
        }

    def detect_duplicate_tests(self, tests_file):
        try:
            test_content = tests_file.read_text()
            tree = ast.parse(test_content)

            test_signatures = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    signature = {
                        'name': node.name,
                        'line': node.lineno,
                        'method_calls': [],
                        'assertions': [],
                        'literals': []
                    }

                    for child in ast.walk(node):
                        if isinstance(child, ast.Call):
                            if isinstance(child.func, ast.Attribute):
                                signature['method_calls'].append(child.func.attr)

                        if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute):
                            if child.func.attr.startswith('assert'):
                                signature['assertions'].append(child.func.attr)

                        if isinstance(child, (ast.Constant, ast.Num, ast.Str)):
                            value = child.value if isinstance(child, ast.Constant) else (
                                child.n if isinstance(child, ast.Num) else child.s
                            )
                            if isinstance(value, (int, float, str)) and value not in [0, 1, '']:
                                signature['literals'].append(value)

                    test_signatures.append(signature)

            duplicates = []
            for i, sig1 in enumerate(test_signatures):
                for sig2 in test_signatures[i+1:]:
                    similarity_score = self._calculate_test_similarity(sig1, sig2)

                    if similarity_score > 0.8:
                        duplicates.append({
                            'test1': sig1['name'],
                            'test1_line': sig1['line'],
                            'test2': sig2['name'],
                            'test2_line': sig2['line'],
                            'similarity': round(similarity_score * 100, 1)
                        })

            return {
                'total_tests_analyzed': len(test_signatures),
                'duplicate_pairs_found': len(duplicates),
                'duplicates': duplicates[:10]
            }

        except Exception as e:
            logger.warning(f"Duplicate detection failed: {e}")
            return {
                'total_tests_analyzed': 0,
                'duplicate_pairs_found': 0,
                'duplicates': [],
                'error': str(e)
            }

    def _calculate_test_similarity(self, sig1, sig2):
        calls1 = set(sig1['method_calls'])
        calls2 = set(sig2['method_calls'])

        if not calls1 and not calls2:
            call_similarity = 1.0
        elif not calls1 or not calls2:
            call_similarity = 0.0
        else:
            call_similarity = len(calls1 & calls2) / len(calls1 | calls2)

        asserts1 = set(sig1['assertions'])
        asserts2 = set(sig2['assertions'])

        if not asserts1 and not asserts2:
            assert_similarity = 1.0
        elif not asserts1 or not asserts2:
            assert_similarity = 0.0
        else:
            assert_similarity = len(asserts1 & asserts2) / len(asserts1 | asserts2)

        lits1 = set(sig1['literals'])
        lits2 = set(sig2['literals'])

        if not lits1 and not lits2:
            lit_similarity = 1.0
        elif not lits1 or not lits2:
            lit_similarity = 0.0
        else:
            lit_similarity = len(lits1 & lits2) / len(lits1 | lits2)

        return (call_similarity * 0.5) + (assert_similarity * 0.3) + (lit_similarity * 0.2)

    def analyze_assertion_quality(self, tests_file):
        try:
            test_content = tests_file.read_text()
            tree = ast.parse(test_content)

            weak_assertions = []
            strong_assertions = []
            assertions_without_message = 0

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    for child in ast.walk(node):
                        if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute):
                            if child.func.attr.startswith('assert'):
                                assertion_type = child.func.attr

                                if assertion_type in ['assertIsNotNone', 'assertTrue', 'assertFalse', 'assertIsNone']:
                                    weak_assertions.append({
                                        'test': node.name,
                                        'line': child.lineno,
                                        'type': assertion_type
                                    })
                                elif assertion_type in ['assertEqual', 'assertAlmostEqual', 'assertGreater',
                                                        'assertLess', 'assertIn', 'assertNotIn']:
                                    strong_assertions.append({
                                        'test': node.name,
                                        'line': child.lineno,
                                        'type': assertion_type
                                    })

                                if len(child.args) < 3:
                                    assertions_without_message += 1

            total_assertions = len(weak_assertions) + len(strong_assertions)

            return {
                'total_assertions': total_assertions,
                'weak_assertions_count': len(weak_assertions),
                'strong_assertions_count': len(strong_assertions),
                'weak_assertions': weak_assertions[:5],
                'assertions_without_message': assertions_without_message,
                'assertion_quality_score': round((len(strong_assertions) / total_assertions * 100) if total_assertions > 0 else 0, 1)
            }

        except Exception as e:
            logger.warning(f"Assertion quality analysis failed: {e}")
            return {
                'total_assertions': 0,
                'weak_assertions_count': 0,
                'strong_assertions_count': 0,
                'weak_assertions': [],
                'assertions_without_message': 0,
                'assertion_quality_score': 0
            }

    def analyze_exception_testing_quality(self, tests_file):
        try:
            test_content = tests_file.read_text()
            tree = ast.parse(test_content)

            exception_tests = []
            tests_with_message_check = 0
            generic_exception_usage = 0

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    for child in ast.walk(node):
                        if isinstance(child, ast.Call):
                            if isinstance(child.func, ast.Attribute) and child.func.attr == 'assertRaises':
                                if child.args:
                                    exc_type = ast.unparse(child.args[0]) if hasattr(ast, 'unparse') else str(child.args[0])

                                    if 'Exception' == exc_type:
                                        generic_exception_usage += 1

                                    exception_tests.append({
                                        'test': node.name,
                                        'line': child.lineno,
                                        'exception_type': exc_type
                                    })

                        if isinstance(child, ast.withitem):
                            if child.optional_vars:
                                tests_with_message_check += 1

            return {
                'exception_tests_count': len(exception_tests),
                'tests_with_message_check': tests_with_message_check,
                'generic_exception_usage': generic_exception_usage,
                'exception_tests': exception_tests[:10],
                'exception_quality_score': round((tests_with_message_check / len(exception_tests) * 100) if exception_tests else 0, 1)
            }

        except Exception as e:
            logger.warning(f"Exception testing quality analysis failed: {e}")
            return {
                'exception_tests_count': 0,
                'tests_with_message_check': 0,
                'generic_exception_usage': 0,
                'exception_tests': [],
                'exception_quality_score': 0
            }

    def analyze_test_independence(self, tests_file):
        try:
            test_content = tests_file.read_text()
            tree = ast.parse(test_content)

            tests_modifying_self = []
            tests_with_class_variables = []
            potential_dependencies = []

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for item in node.body:
                        if isinstance(item, ast.Assign):
                            for test in node.body:
                                if isinstance(test, ast.FunctionDef) and test.name.startswith('test_'):
                                    tests_with_class_variables.append({
                                        'test': test.name,
                                        'line': test.lineno
                                    })

                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    for child in ast.walk(node):
                        if isinstance(child, ast.Assign):
                            for target in child.targets:
                                if isinstance(target, ast.Attribute):
                                    if isinstance(target.value, ast.Name) and target.value.id == 'self':
                                        tests_modifying_self.append({
                                            'test': node.name,
                                            'line': child.lineno,
                                            'attribute': target.attr
                                        })

            independence_score = 100
            if tests_modifying_self:
                independence_score -= len(tests_modifying_self) * 10
            if tests_with_class_variables:
                independence_score -= 20
            independence_score = max(0, independence_score)

            return {
                'tests_modifying_self_count': len(tests_modifying_self),
                'tests_with_class_variables_count': len(tests_with_class_variables),
                'tests_modifying_self': tests_modifying_self[:5],
                'independence_score': independence_score,
                'is_independent': len(tests_modifying_self) == 0 and len(tests_with_class_variables) == 0
            }

        except Exception as e:
            logger.warning(f"Test independence analysis failed: {e}")
            return {
                'tests_modifying_self_count': 0,
                'tests_with_class_variables_count': 0,
                'tests_modifying_self': [],
                'independence_score': 100,
                'is_independent': True
            }

    def analyze_test_naming_quality(self, tests_file):
        try:
            test_content = tests_file.read_text()
            tree = ast.parse(test_content)

            test_names = []
            short_names = []
            descriptive_names = []
            naming_patterns = {
                'should': 0,
                'when': 0,
                'given': 0,
                'test_': 0,
                'with': 0,
                'returns': 0,
                'raises': 0
            }

            action_verbs = ['add', 'remove', 'calculate', 'get', 'set', 'update', 'delete',
                           'create', 'validate', 'check', 'verify', 'apply', 'clear']

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    name = node.name
                    test_names.append(name)

                    if len(name) < 15:
                        short_names.append({'name': name, 'length': len(name)})

                    name_lower = name.lower()
                    for pattern in naming_patterns:
                        if pattern in name_lower:
                            naming_patterns[pattern] += 1

                    if any(verb in name_lower for verb in action_verbs):
                        descriptive_names.append(name)

            total_tests = len(test_names)
            avg_name_length = sum(len(n) for n in test_names) / total_tests if total_tests > 0 else 0

            naming_quality_score = 0
            if total_tests > 0:
                descriptive_ratio = len(descriptive_names) / total_tests
                naming_quality_score = round(descriptive_ratio * 100, 1)

            return {
                'total_tests': total_tests,
                'average_name_length': round(avg_name_length, 1),
                'short_names_count': len(short_names),
                'descriptive_names_count': len(descriptive_names),
                'naming_patterns': naming_patterns,
                'naming_quality_score': naming_quality_score,
                'short_names': short_names[:5]
            }

        except Exception as e:
            logger.warning(f"Test naming quality analysis failed: {e}")
            return {
                'total_tests': 0,
                'average_name_length': 0,
                'short_names_count': 0,
                'descriptive_names_count': 0,
                'naming_patterns': {},
                'naming_quality_score': 0,
                'short_names': []
            }

    def detect_code_smells(self, tests_file):
        try:
            test_content = tests_file.read_text()
            tree = ast.parse(test_content)

            smells = {
                'tests_without_assertions': [],
                'very_long_tests': [],  # > 30 LOC
                'tests_with_try_except': [],
                'tests_with_sleep': [],
                'magic_numbers': [],
                'commented_code_lines': 0
            }

            lines = test_content.split('\n')
            smells['commented_code_lines'] = sum(1 for line in lines if line.strip().startswith('#'))

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    has_assertion = False
                    has_try_except = False
                    has_sleep = False
                    magic_nums = set()

                    test_length = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0

                    for child in ast.walk(node):
                        if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute):
                            if child.func.attr.startswith('assert'):
                                has_assertion = True

                        if isinstance(child, ast.Try):
                            has_try_except = True

                        if isinstance(child, ast.Call):
                            if isinstance(child.func, ast.Attribute) and child.func.attr == 'sleep':
                                has_sleep = True
                            elif isinstance(child.func, ast.Name) and child.func.id == 'sleep':
                                has_sleep = True

                        if isinstance(child, (ast.Constant, ast.Num)):
                            value = child.value if isinstance(child, ast.Constant) else child.n
                            if isinstance(value, (int, float)) and abs(value) > 1 and value not in [100, 1000, 10000]:
                                magic_nums.add(value)

                    if not has_assertion:
                        smells['tests_without_assertions'].append({
                            'test': node.name,
                            'line': node.lineno
                        })

                    if test_length > 30:
                        smells['very_long_tests'].append({
                            'test': node.name,
                            'line': node.lineno,
                            'length': test_length
                        })

                    if has_try_except:
                        smells['tests_with_try_except'].append({
                            'test': node.name,
                            'line': node.lineno
                        })

                    if has_sleep:
                        smells['tests_with_sleep'].append({
                            'test': node.name,
                            'line': node.lineno
                        })

                    if len(magic_nums) > 3:
                        smells['magic_numbers'].append({
                            'test': node.name,
                            'count': len(magic_nums),
                            'numbers': list(magic_nums)[:10]
                        })

            smell_score = 100
            smell_score -= len(smells['tests_without_assertions']) * 20
            smell_score -= len(smells['very_long_tests']) * 5
            smell_score -= len(smells['tests_with_try_except']) * 10
            smell_score -= len(smells['tests_with_sleep']) * 15
            smell_score -= min(smells['commented_code_lines'], 20)
            smell_score = max(0, smell_score)

            return {
                'smells': smells,
                'smell_score': smell_score,
                'total_smells_found': sum([
                    len(smells['tests_without_assertions']),
                    len(smells['very_long_tests']),
                    len(smells['tests_with_try_except']),
                    len(smells['tests_with_sleep'])
                ])
            }

        except Exception as e:
            logger.warning(f"Code smell detection failed: {e}")
            return {
                'smells': {},
                'smell_score': 100,
                'total_smells_found': 0
            }

    def analyze_test_quality(self, test_content):
        quality = {
            'has_setup_teardown': False,
            'uses_assertions': 0,
            'tests_with_multiple_assertions': 0,
            'uses_context_managers': 0,
            'has_edge_case_testing': False,
            'has_error_testing': 0,
            'average_test_length': 0
        }
        
        lines = test_content.split('\n')
        test_methods = []
        current_test = []
        in_test = False
        
        for line in lines:
            if line.strip().startswith('def test_'):
                if current_test:
                    test_methods.append(current_test)
                current_test = [line]
                in_test = True
            elif in_test:
                if line.strip().startswith('def ') and not line.strip().startswith('def test_'):
                    in_test = False
                    test_methods.append(current_test)
                    current_test = []
                else:
                    current_test.append(line)
        
        if current_test:
            test_methods.append(current_test)
        
        total_assertions = 0
        for test in test_methods:
            test_text = '\n'.join(test)
            
            assertions = test_text.count('assert')
            total_assertions += assertions
            
            if assertions > 1:
                quality['tests_with_multiple_assertions'] += 1
                
            if 'with ' in test_text and ('assertRaises' in test_text or 'pytest.raises' in test_text):
                quality['uses_context_managers'] += 1
                
            if any(keyword in test_text.lower() for keyword in ['assertraises', 'exception', 'error', 'valueerror']):
                quality['has_error_testing'] += 1
        
        quality['uses_assertions'] = total_assertions
        quality['average_test_length'] = sum(len(test) for test in test_methods) / len(test_methods) if test_methods else 0
        
        if 'def setUp' in test_content or 'def tearDown' in test_content:
            quality['has_setup_teardown'] = True
            
        return quality
    
    def generate_comprehensive_summary(self, analysis_results, experiment_data):
        summary = {
            'model': experiment_data['model'],
            'strategy': experiment_data['strategy'],
            'context_type': experiment_data['context_type'],
            'timestamp': experiment_data['timestamp'],
            'response_time': experiment_data['response_time']
        }
        
        if 'compilation' in analysis_results and analysis_results['compilation']:
            comp = analysis_results['compilation']
            summary['compilation_success_rate'] = 100 if comp['compilation_success'] else 0
            summary['execution_success_rate'] = 100 if comp.get('execution_success', False) else 0
            summary['tests_generated'] = comp.get('tests_run', 0)
            summary['tests_passed'] = comp.get('tests_passed', 0)
            summary['tests_failed'] = comp.get('tests_failed', 0)
            
            if summary['tests_generated'] > 0:
                summary['test_success_rate'] = round((summary['tests_passed'] / summary['tests_generated']) * 100, 1)
            else:
                summary['test_success_rate'] = 0
        
        if 'coverage' in analysis_results and analysis_results['coverage']:
            cov = analysis_results['coverage']
            summary['statement_coverage'] = cov.get('coverage_percent', 0)
            summary['branch_coverage'] = cov.get('branch_coverage_percent', 0)
            summary['missing_statements'] = cov.get('missing', 0)
            summary['total_statements'] = cov.get('statements', 0)
        
        if 'mutation' in analysis_results and analysis_results['mutation']:
            mut = analysis_results['mutation']
            summary['mutation_score'] = mut.get('mutation_score', 0)
            summary['mutants_killed'] = mut.get('killed', 0)
            summary['mutants_survived'] = mut.get('survived', 0)
            summary['total_mutants'] = mut.get('total_mutants', 0)
        
        if 'scenarios' in analysis_results and analysis_results['scenarios']:
            scen = analysis_results['scenarios']
            summary['total_test_methods'] = scen.get('total_test_methods', 0)

            quality = scen.get('quality_metrics', {})
            summary['total_assertions'] = quality.get('uses_assertions', 0)
            summary['tests_with_error_handling'] = quality.get('has_error_testing', 0)
            summary['average_test_length'] = round(quality.get('average_test_length', 0), 1)
            summary['has_setup_teardown'] = quality.get('has_setup_teardown', False)
            summary['tests_with_multiple_assertions'] = quality.get('tests_with_multiple_assertions', 0)

            tested_methods = scen.get('tested_methods', {})
            summary['methods_tested_count'] = tested_methods.get('methods_tested_count', 0)
            summary['total_methods'] = tested_methods.get('total_methods', 12)
            summary['method_coverage_rate'] = tested_methods.get('method_coverage_rate', 0)

            duplicates = scen.get('duplicates', {})
            summary['duplicate_tests_found'] = duplicates.get('duplicate_pairs_found', 0)

            if summary['total_test_methods'] > 0:
                summary['avg_assertions_per_test'] = round(summary['total_assertions'] / summary['total_test_methods'], 2)
            else:
                summary['avg_assertions_per_test'] = 0

            assertion_quality = scen.get('assertion_quality', {})
            summary['assertion_quality_score'] = assertion_quality.get('assertion_quality_score', 0)
            summary['weak_assertions_count'] = assertion_quality.get('weak_assertions_count', 0)
            summary['strong_assertions_count'] = assertion_quality.get('strong_assertions_count', 0)

            exception_quality = scen.get('exception_quality', {})
            summary['exception_quality_score'] = exception_quality.get('exception_quality_score', 0)
            summary['exception_tests_count'] = exception_quality.get('exception_tests_count', 0)
            summary['tests_with_message_check'] = exception_quality.get('tests_with_message_check', 0)

            independence = scen.get('independence', {})
            summary['independence_score'] = independence.get('independence_score', 100)
            summary['is_independent'] = independence.get('is_independent', True)

            naming_quality = scen.get('naming_quality', {})
            summary['naming_quality_score'] = naming_quality.get('naming_quality_score', 0)
            summary['average_name_length'] = naming_quality.get('average_name_length', 0)

            code_smells = scen.get('code_smells', {})
            summary['smell_score'] = code_smells.get('smell_score', 100)
            summary['total_smells_found'] = code_smells.get('total_smells_found', 0)

            quality_scores = [
                summary.get('assertion_quality_score', 0) * 0.25,
                summary.get('exception_quality_score', 0) * 0.15,
                summary.get('independence_score', 100) * 0.15,
                summary.get('naming_quality_score', 0) * 0.15,
                summary.get('smell_score', 100) * 0.15,
                (100 - min(summary.get('duplicate_tests_found', 0), 50) * 2) * 0.15
            ]
            summary['overall_quality_score'] = round(sum(quality_scores), 1)

        return summary
    
    def save_analysis_results(self, result_dir, analysis_results, experiment_data):
        analysis_file = result_dir / "analysis_results.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        self.generate_csv_analysis(result_dir, analysis_results, experiment_data)
        
        self.generate_markdown_summary(result_dir, analysis_results, experiment_data)
        
        logger.info(f"✓ Analysis results saved to {result_dir}")
    
    def generate_csv_analysis(self, result_dir, analysis_results, experiment_data):
        import csv

        model_name = experiment_data['model'].replace('.', '').replace(' ', '-')
        csv_file = result_dir / f"analiza-{model_name}.csv"

        rows = []

        if 'scenarios' in analysis_results and analysis_results['scenarios']:
            tested_methods = analysis_results['scenarios'].get('tested_methods', {})
            method_calls = tested_methods.get('method_call_counts', {})

            for method, count in method_calls.items():
                rows.append({
                    'Category': 'Tested Method',
                    'Name': method,
                    'Count': count,
                    'Details': f'Called {count} times in tests'
                })

            duplicates = analysis_results['scenarios'].get('duplicates', {})
            for dup in duplicates.get('duplicates', []):
                rows.append({
                    'Category': 'Potential Duplicate',
                    'Name': f"{dup['test1']} <-> {dup['test2']}",
                    'Count': dup['similarity'],
                    'Details': f"Similarity: {dup['similarity']}% (lines {dup['test1_line']}, {dup['test2_line']})"
                })

        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Category', 'Name', 'Count', 'Details'])
            writer.writeheader()
            writer.writerows(rows)

        logger.info(f"✓ CSV analysis saved to {csv_file}")
    
    def generate_markdown_summary(self, result_dir, analysis_results, experiment_data):
        summary = analysis_results.get('summary', {})
        model_name = experiment_data['model']
        strategy = experiment_data['strategy']
        context = experiment_data['context_type']

        md_file = result_dir / f"podsumowanie-{model_name.replace('.', '').replace(' ', '-')}.md"

        content = f"""# Unit Test Coverage Analysis Summary (Model: {model_name})
# Context: {context}
# Prompt Strategy: {strategy.replace('_', '-')}

## coverage.py
- missing: {summary.get('missing_statements', 'N/A')}
- coverage: {summary.get('statement_coverage', 'N/A')}%

## mutmut.py
⠋ {summary.get('total_mutants', 0)}/{summary.get('total_mutants', 0)}  🎉 {summary.get('mutants_killed', 0)} 🫥 0  ⏰ 0  🤔 0  🙁 {summary.get('mutants_survived', 0)}  🔇 0

## Results
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

## Automatically generated by LLM Testing Automation
- Response time: {summary.get('response_time', 0):.2f}s
- Generated at: {summary.get('timestamp', 'N/A')}

"""

        md_file.write_text(content, encoding='utf-8')
        logger.info(f"✓ Markdown summary saved to {md_file}")