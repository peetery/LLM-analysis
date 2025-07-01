"""
Main LLM experiments orchestrator
"""
import json
import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime
import shutil

from openai_client import OpenAIClient
from anthropic_client import AnthropicClient
from deepseek_client import DeepseekClient
from google_client import GoogleClient
from prompt_strategies import SimplePrompting, ChainOfThoughtPrompting

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExperimentRunner:
    """Orkiestrator eksperymentów LLM"""
    
    def __init__(self, base_results_dir="prompts_results"):
        self.base_results_dir = Path(base_results_dir)
        self.current_experiment = None
        
        # Mapowanie modeli na klienty
        self.model_clients = {
            'gpt-4': OpenAIClient,
            'gpt-4.5': OpenAIClient,
            'gpt-o3': OpenAIClient,
            'gpt-o4-mini-high': OpenAIClient,
            'claude-3.7-sonnet': AnthropicClient,
            'deepseek': DeepseekClient,
            'gemini-2.5-pro': GoogleClient
        }
    
    def run_single_experiment(self, model_name, strategy_name, context_type, headless=True):
        """Uruchamia pojedynczy eksperyment"""
        logger.info(f"Starting experiment: {model_name} - {strategy_name} - {context_type}")
        
        # Sprawdź czy model jest obsługiwany
        if model_name not in self.model_clients or self.model_clients[model_name] is None:
            logger.error(f"Model {model_name} not supported yet")
            return None
        
        # Utwórz katalog wyników
        result_dir = self.base_results_dir / strategy_name / context_type / model_name
        result_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicjalizuj klienta LLM
        client_class = self.model_clients[model_name]
        
        try:
            # Always use attach mode now - all models benefit from it
            llm_client = client_class(model_name=model_name, headless=headless, attach_to_existing=True, debug_port=9222)
            
            with llm_client:
                # Auto-navigate to the correct model URL with direct model selection
                model_urls = {
                    'gpt-4.5': 'https://chatgpt.com/?model=gpt-4.5',
                    'gpt-o3': 'https://chatgpt.com/?model=o3',
                    'gpt-o4-mini-high': 'https://chatgpt.com/?model=gpt-4o-mini',
                    'claude-3.7-sonnet': 'https://claude.ai/',
                    'deepseek': 'https://chat.deepseek.com/',
                    'gemini-2.5-pro': 'https://gemini.google.com/'
                }
                
                target_url = model_urls.get(model_name, 'https://google.com')
                logger.info(f"📍 Navigating to {target_url} for model: {model_name}")
                llm_client.driver.get(target_url)
                time.sleep(5)  # Dłuższy czas na załadowanie modelu
                
                # Login
                if not llm_client.login():
                    logger.error("Failed to login")
                    return None
                
                # Sprawdź ostatecznie czy właściwy model jest wybrany
                if hasattr(llm_client, 'get_current_model'):
                    final_model = llm_client.get_current_model()
                    logger.info(f"🎯 Final model verification: {final_model} (expected: {model_name})")
                    
                    if hasattr(llm_client, 'is_correct_model') and hasattr(llm_client, 'get_target_model_name'):
                        target_variants = llm_client.get_target_model_name()
                        if not llm_client.is_correct_model(final_model, target_variants):
                            logger.error(f"❌ CRITICAL: WRONG MODEL! Expected: {target_variants}, Got: {final_model}")
                            logger.error(f"❌ CRITICAL: Experiment results will be INVALID for {model_name}!")
                            logger.error(f"❌ CRITICAL: ChatGPT auto-switched models - this is a known issue.")
                            
                            # Możemy kontynuować ale z ostrzeżeniem
                            logger.warning(f"⚠️  CONTINUING with wrong model - results will be labeled as {final_model} not {model_name}")
                        else:
                            logger.info(f"✅ SUCCESS: Correct model confirmed: {final_model}")
                
                # Start strategy
                if strategy_name == "simple_prompting":
                    strategy = SimplePrompting()
                elif strategy_name == "chain_of_thought_prompting":
                    strategy = ChainOfThoughtPrompting()
                else:
                    logger.error(f"Unknown strategy: {strategy_name}")
                    return None
                
                # Rozpocznij nowy chat
                llm_client.start_new_chat()
                
                # Wykonaj strategię
                strategy_result = strategy.execute(llm_client, context_type)
                
                if not strategy_result:
                    logger.error("Strategy execution failed")
                    return None
                
                # Sprawdź jaki model był rzeczywiście użyty
                actual_model_used = model_name  # Default
                if hasattr(llm_client, 'get_current_model'):
                    detected_model = llm_client.get_current_model()
                    if detected_model and detected_model != "unknown":
                        actual_model_used = detected_model
                        logger.info(f"📝 Recording actual model used: {actual_model_used}")
                
                # Zapisz wyniki z rzeczywistym modelem
                experiment_results = self.save_experiment_results(
                    result_dir, strategy_result, actual_model_used, strategy_name, context_type
                )
                
                # Uruchom analizę
                analysis_results = self.run_analysis(result_dir, experiment_results)
                
                return {
                    'experiment': experiment_results,
                    'analysis': analysis_results
                }
                
        except Exception as e:
            logger.error(f"Experiment failed: {e}")
            return None
    
    def save_experiment_results(self, result_dir, strategy_result, model_name, strategy_name, context_type):
        """Zapisuje wyniki eksperymentu"""
        timestamp = datetime.now().isoformat()
        
        # Wyciągnij kod testów
        if strategy_name == "simple_prompting":
            test_code = self.extract_test_code(strategy_result['response'])
            response_time = strategy_result['response_time']
        else:  # chain_of_thought
            test_code = self.extract_test_code(strategy_result['final_response'])
            response_time = strategy_result['total_response_time']
        
        if not test_code:
            logger.error("Failed to extract test code from response")
            return None
        
        # Zapisz testy
        tests_file = result_dir / "tests.py"
        tests_file.write_text(test_code)
        
        # Skopiuj do mutmut_test.py
        mutmut_test_file = result_dir / "mutmut_test.py"
        shutil.copy2(tests_file, mutmut_test_file)
        
        # ZAWSZE kopiuj order_calculator.py do katalogu testów
        source_file = Path("../order_calculator.py")  # Go up from automation/
        if not source_file.exists():
            source_file = Path("../../order_calculator.py")  # Try parent of parent
        if not source_file.exists():
            source_file = Path("order_calculator.py")  # Try current directory
            
        if source_file.exists():
            dest_file = result_dir / "order_calculator.py"
            shutil.copy2(source_file, dest_file)
            logger.info(f"✓ Copied {source_file} to test directory")
        else:
            logger.error("✗ order_calculator.py not found - tests will fail")
        
        # Zapisz pełne wyniki
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
    
    def extract_test_code(self, response_text):
        """Extract test code from LLM response with UI artifact cleaning"""
        import re
        
        def clean_code_block(code):
            """Clean ChatGPT UI artifacts from code"""
            lines = code.split('\n')
            cleaned_lines = []
            
            for line in lines:
                original_line = line
                line_stripped = line.strip()
                
                # Skip ChatGPT UI elements
                ui_artifacts = [
                    'python', 'kopiuj', 'edytuj', 'copy', 'edit', 'skopiuj',
                    'bash', 'shell', 'powershell', 'cmd', 'javascript', 'js',
                    'html', 'css', 'sql', 'json', 'xml', 'yaml'
                ]
                
                if line_stripped.lower() in ui_artifacts:
                    continue
                    
                # Skip lines that are just language indicators
                if line_stripped.startswith('```'):
                    continue
                    
                # Skip empty lines at the beginning
                if not cleaned_lines and not line_stripped:
                    continue
                    
                cleaned_lines.append(original_line)
            
            # Remove trailing empty lines
            while cleaned_lines and not cleaned_lines[-1].strip():
                cleaned_lines.pop()
                
            return '\n'.join(cleaned_lines)
        
        # Look for Python code blocks
        code_blocks = re.findall(r'```python\n(.*?)\n```', response_text, re.DOTALL)
        if code_blocks:
            return clean_code_block(code_blocks[0])
        
        # Look for code blocks without language specification
        code_blocks = re.findall(r'```\n(.*?)\n```', response_text, re.DOTALL)
        if code_blocks:
            for block in code_blocks:
                cleaned_block = clean_code_block(block)
                if 'unittest' in cleaned_block or 'def test' in cleaned_block:
                    return cleaned_block
        
        # Last resort - find code starting with import or class
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
            code_lines = lines[code_start:]
            code = '\n'.join(code_lines)
            return clean_code_block(code)
        
        return None
    
    def run_analysis(self, result_dir, experiment_data):
        """Uruchamia kompletną analizę testów"""
        tests_file = Path(experiment_data['test_file'])
        
        if not tests_file.exists():
            logger.error(f"Test file not found: {tests_file}")
            return None
        
        analysis_results = {}
        
        # 1. Test kompilacji i uruchomienia
        compilation_result = self.test_compilation_and_execution(tests_file)
        analysis_results['compilation'] = compilation_result
        
        if not compilation_result['compilation_success']:
            logger.error("Tests do not compile")
            # Nadal kontynuuj analizę scenariuszy
        
        # 2. Uruchom coverage (jeśli kompilacja przeszła)
        if compilation_result['compilation_success']:
            coverage_results = self.run_coverage_analysis(result_dir, tests_file)
            analysis_results['coverage'] = coverage_results
        else:
            analysis_results['coverage'] = None
        
        # 3. Uruchom mutation testing (jeśli kompilacja przeszła)
        if compilation_result['compilation_success']:
            mutation_results = self.run_mutation_testing(result_dir)
            analysis_results['mutation'] = mutation_results
        else:
            analysis_results['mutation'] = None
        
        # 4. Analiza scenariuszy (zawsze wykonaj)
        scenario_analysis = self.analyze_test_scenarios(tests_file)
        analysis_results['scenarios'] = scenario_analysis
        
        # 5. Generuj kompletne podsumowanie
        summary = self.generate_comprehensive_summary(analysis_results, experiment_data)
        analysis_results['summary'] = summary
        
        # 6. Zapisz wyniki w różnych formatach
        self.save_analysis_results(result_dir, analysis_results, experiment_data)
        
        return analysis_results
    
    def test_compilation(self, tests_file):
        """Test if tests compile (order_calculator.py already copied)"""
        try:
            result = subprocess.run(
                ['python', '-m', 'py_compile', tests_file.name],  # Use relative name, not full path
                cwd=tests_file.parent,  # Run in test directory
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
        """Run code coverage analysis (order_calculator.py already copied)"""
        try:
            # Run tests with coverage including branch coverage
            cmd = [
                'python', '-m', 'coverage', 'run', 
                '--source=.', '--branch', '-m', 'unittest', 
                tests_file.stem
            ]
            
            result = subprocess.run(
                cmd,
                cwd=result_dir,  # Run in test directory with order_calculator.py
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                logger.error(f"Coverage run failed: {result.stderr}")
                return None
            
            # Generuj raport
            report_result = subprocess.run(
                ['python', '-m', 'coverage', 'report'],
                cwd=result_dir,
                capture_output=True,
                text=True
            )
            
            # Generuj HTML
            subprocess.run(
                ['python', '-m', 'coverage', 'html'],
                cwd=result_dir,
                capture_output=True,
                text=True
            )
            
            # Parsuj wyniki
            coverage_data = self.parse_coverage_report(report_result.stdout)
            return coverage_data
            
        except Exception as e:
            logger.error(f"Coverage analysis failed: {e}")
            return None
    
    def parse_coverage_report(self, coverage_output):
        """Parsuje szczegółowe wyniki coverage"""
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
                if len(parts) >= 4:
                    try:
                        coverage_data['statements'] = int(parts[1])
                        coverage_data['missing'] = int(parts[2])
                        coverage_data['coverage_percent'] = int(parts[3].replace('%', ''))
                        
                        # Jeśli jest kolumna "Cover" (branch coverage)
                        if len(parts) >= 5 and '%' in parts[4]:
                            coverage_data['branch_coverage_percent'] = int(parts[4].replace('%', ''))
                            
                    except (ValueError, IndexError):
                        pass
                        
        # Spróbuj wyciągnąć informacje o branch coverage z innych linii
        for line in lines:
            if 'branch' in line.lower() and '%' in line:
                try:
                    # Szukaj wzorca jak "82% branch coverage"
                    import re
                    match = re.search(r'(\d+)%.*branch', line)
                    if match:
                        coverage_data['branch_coverage_percent'] = int(match.group(1))
                except:
                    pass
        
        return coverage_data if coverage_data['statements'] > 0 else None
    
    def run_mutation_testing(self, result_dir):
        """Run mutation testing"""
        try:
            # Find mutants directory - check parent directories
            current_dir = Path(".")
            mutants_dir = None
            
            # Look in current directory and parent directories
            for i in range(3):  # Check up to 3 levels up
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
                    'mutation_score': 0,
                    'status': 'skipped'
                }
            
            # Skopiuj test do katalogu mutants/tests
            test_src = result_dir / "mutmut_test.py"
            test_dst = mutants_dir / "tests" / "mutmut_test.py"
            
            test_dst.parent.mkdir(exist_ok=True)
            shutil.copy2(test_src, test_dst)
            
            # Uruchom mutmut
            result = subprocess.run(
                ['python', '-m', 'mutmut', 'run'],
                cwd=mutants_dir,
                capture_output=True,
                text=True,
                timeout=600  # 10 minut timeout
            )
            
            # Pobierz wyniki
            results_result = subprocess.run(
                ['python', '-m', 'mutmut', 'results'],
                cwd=mutants_dir,
                capture_output=True,
                text=True
            )
            
            # Zapisz wyniki do pliku
            mutmut_results_file = result_dir / "mutmut_results.txt"
            mutmut_results_file.write_text(results_result.stdout)
            
            # Parsuj statystyki
            stats = self.parse_mutmut_results(results_result.stdout)
            
            # Zapisz statystyki
            stats_file = result_dir / "mutmut-stats.json"
            with open(stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
            
            return stats
            
        except Exception as e:
            logger.error(f"Mutation testing failed: {e}")
            return None
    
    def parse_mutmut_results(self, mutmut_output):
        """Parsuje szczegółowe wyniki mutmut"""
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
        
        # Szukaj wzorca emoji jak w przykładzie: "⠋ 217/217  🎉 94 🫥 0  ⏰ 0  🤔 0  🙁 123  🔇 0"
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
            
            # Oblicz mutation score
            if progress_total > 0:
                stats['mutation_score'] = round((killed / progress_total) * 100, 1)
        
        # Fallback - szukaj innych wzorców
        if stats['total_mutants'] == 0:
            # Szukaj wzorców jak "Total: 217, killed: 94, survived: 123"
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
    
    
    def run_batch_experiments(self, config_file):
        """Uruchamia serię eksperymentów z pliku konfiguracyjnego"""
        with open(config_file) as f:
            config = json.load(f)
        
        results = []
        
        for experiment in config['experiments']:
            model = experiment['model']
            strategy = experiment['strategy']
            context = experiment['context']
            
            logger.info(f"Running experiment: {model} - {strategy} - {context}")
            
            result = self.run_single_experiment(
                model, strategy, context, 
                headless=config.get('headless', True)
            )
            
            if result:
                results.append(result)
                logger.info("Experiment completed successfully")
            else:
                logger.error("Experiment failed")
            
            # Przerwa między eksperymentami
            time.sleep(config.get('delay_between_experiments', 10))
        
        return results
    
    def test_compilation_and_execution(self, tests_file):
        """Test if tests compile and execute (order_calculator.py already copied)"""
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
            # 1. Test kompilacji
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
                
                # 2. Test uruchomienia
                unittest_result = subprocess.run(
                    ['python', '-m', 'unittest', tests_file.stem, '-v'],
                    cwd=tests_file.parent,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                # Parsuj wyniki unittest
                self.parse_unittest_results(unittest_result.stderr, result)
                
            else:
                result['compilation_errors'] = [compile_result.stderr]
                logger.error(f"✗ Compilation failed: {compile_result.stderr}")
                
        except Exception as e:
            logger.error(f"Compilation/execution test failed: {e}")
            result['compilation_errors'] = [str(e)]
            
        return result
    
    def parse_unittest_results(self, unittest_output, result):
        """Parsuje wyniki unittest"""
        lines = unittest_output.strip().split('\n')
        
        for line in lines:
            if 'Ran' in line and 'test' in line:
                # Przykład: "Ran 25 tests in 0.012s"
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
        """Wyciąga liczbę z tekstu po prefiksie"""
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
        """Kompletna analiza pokrycia scenariuszy testowych"""
        # Załaduj scenariusze z pliku
        scenarios_file = Path("../scenariusze_testowe.md")  # Go up from automation/
        if not scenarios_file.exists():
            scenarios_file = Path("scenariusze_testowe.md")  # Try current directory
        if not scenarios_file.exists():
            scenarios_file = Path("../../scenariusze_testowe.md")  # Try parent of parent
            
        if not scenarios_file.exists():
            logger.warning("Scenarios file not found - scenario analysis will be limited")
            test_content = tests_file.read_text()
            test_methods = test_content.count('def test_')
            return {
                'total_test_methods': test_methods,
                'estimated_scenario_coverage': min(test_methods, 54),
                'scenarios_file_found': False
            }
        
        # Analiza pokrycia scenariuszy
        test_content = tests_file.read_text()
        scenarios_content = scenarios_file.read_text()
        
        # Zlicz wszystkie metody testowe
        test_methods = test_content.count('def test_')
        
        # Zaawansowana analiza pokrycia scenariuszy
        covered_scenarios = self.detect_covered_scenarios(test_content)
        
        # Analiza jakości testów
        quality_metrics = self.analyze_test_quality(test_content)
        
        return {
            'total_test_methods': test_methods,
            'covered_scenarios': covered_scenarios,
            'quality_metrics': quality_metrics,
            'scenarios_file_found': True,
            'total_defined_scenarios': 54  # Z analizy pliku scenariusze_testowe.md
        }
    
    def detect_covered_scenarios(self, test_content):
        """Wykrywa które scenariusze są pokryte przez testy"""
        covered = {
            'init_scenarios': 0,
            'add_item_scenarios': 0,
            'remove_item_scenarios': 0,
            'get_subtotal_scenarios': 0,
            'apply_discount_scenarios': 0,
            'calculate_shipping_scenarios': 0,
            'calculate_tax_scenarios': 0,
            'calculate_total_scenarios': 0,
            'total_items_scenarios': 0,
            'list_items_scenarios': 0,
            'is_empty_scenarios': 0,
            'clear_order_scenarios': 0,
            'corner_cases': 0,
            'performance_tests': 0,
            'precision_tests': 0
        }
        
        # Wykryj scenariusze na podstawie nazw testów i ich zawartości
        test_lines = test_content.lower().split('\n')
        
        for line in test_lines:
            if 'def test_' in line:
                test_name = line.strip()
                
                # Kategoryzuj testy
                if any(keyword in test_name for keyword in ['init', 'initialization', '__init__']):
                    covered['init_scenarios'] += 1
                elif 'add_item' in test_name:
                    covered['add_item_scenarios'] += 1
                elif 'remove_item' in test_name:
                    covered['remove_item_scenarios'] += 1
                elif 'subtotal' in test_name:
                    covered['get_subtotal_scenarios'] += 1
                elif 'discount' in test_name:
                    covered['apply_discount_scenarios'] += 1
                elif 'shipping' in test_name:
                    covered['calculate_shipping_scenarios'] += 1
                elif 'tax' in test_name:
                    covered['calculate_tax_scenarios'] += 1
                elif 'total' in test_name and 'calculate' in test_name:
                    covered['calculate_total_scenarios'] += 1
                elif 'total_items' in test_name:
                    covered['total_items_scenarios'] += 1
                elif 'list_items' in test_name:
                    covered['list_items_scenarios'] += 1
                elif 'is_empty' in test_name:
                    covered['is_empty_scenarios'] += 1
                elif 'clear' in test_name:
                    covered['clear_order_scenarios'] += 1
                    
                # Wykryj corner cases
                if any(keyword in test_name for keyword in ['negative', 'zero', 'invalid', 'empty', 'none', 'error']):
                    covered['corner_cases'] += 1
                    
                # Wykryj testy wydajności
                if any(keyword in test_name for keyword in ['performance', 'stress', 'large', 'many', '1000']):
                    covered['performance_tests'] += 1
                    
                # Wykryj testy precyzji
                if any(keyword in test_name for keyword in ['precision', 'float', 'decimal', 'accuracy']):
                    covered['precision_tests'] += 1
        
        return covered
    
    def analyze_test_quality(self, test_content):
        """Analizuje jakość testów"""
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
        
        # Analiza każdego testu
        total_assertions = 0
        for test in test_methods:
            test_text = '\n'.join(test)
            
            # Zlicz asercje
            assertions = test_text.count('assert')
            total_assertions += assertions
            
            if assertions > 1:
                quality['tests_with_multiple_assertions'] += 1
                
            # Wykryj context managery (with statements)
            if 'with ' in test_text and ('assertRaises' in test_text or 'pytest.raises' in test_text):
                quality['uses_context_managers'] += 1
                
            # Wykryj testy błędów
            if any(keyword in test_text.lower() for keyword in ['assertraises', 'exception', 'error', 'valueerror']):
                quality['has_error_testing'] += 1
        
        quality['uses_assertions'] = total_assertions
        quality['average_test_length'] = sum(len(test) for test in test_methods) / len(test_methods) if test_methods else 0
        
        # Wykryj setUp/tearDown
        if 'def setUp' in test_content or 'def tearDown' in test_content:
            quality['has_setup_teardown'] = True
            
        return quality
    
    def generate_comprehensive_summary(self, analysis_results, experiment_data):
        """Generuje kompletne podsumowanie analizy"""
        summary = {
            'model': experiment_data['model'],
            'strategy': experiment_data['strategy'],
            'context_type': experiment_data['context_type'],
            'timestamp': experiment_data['timestamp'],
            'response_time': experiment_data['response_time']
        }
        
        # Wyniki kompilacji
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
        
        # Wyniki coverage
        if 'coverage' in analysis_results and analysis_results['coverage']:
            cov = analysis_results['coverage']
            summary['statement_coverage'] = cov.get('coverage_percent', 0)
            summary['branch_coverage'] = cov.get('branch_coverage_percent', 0)
            summary['missing_statements'] = cov.get('missing', 0)
            summary['total_statements'] = cov.get('statements', 0)
        
        # Wyniki mutation testing
        if 'mutation' in analysis_results and analysis_results['mutation']:
            mut = analysis_results['mutation']
            summary['mutation_score'] = mut.get('mutation_score', 0)
            summary['mutants_killed'] = mut.get('killed', 0)
            summary['mutants_survived'] = mut.get('survived', 0)
            summary['total_mutants'] = mut.get('total_mutants', 0)
        
        # Wyniki scenariuszy
        if 'scenarios' in analysis_results and analysis_results['scenarios']:
            scen = analysis_results['scenarios']
            summary['total_test_methods'] = scen.get('total_test_methods', 0)
            summary['covered_scenarios_count'] = sum(scen.get('covered_scenarios', {}).values())
            summary['total_defined_scenarios'] = scen.get('total_defined_scenarios', 54)
            
            if summary['total_defined_scenarios'] > 0:
                summary['scenario_coverage_rate'] = round((summary['covered_scenarios_count'] / summary['total_defined_scenarios']) * 100, 1)
            else:
                summary['scenario_coverage_rate'] = 0
                
            # Jakość testów
            quality = scen.get('quality_metrics', {})
            summary['total_assertions'] = quality.get('uses_assertions', 0)
            summary['tests_with_error_handling'] = quality.get('has_error_testing', 0)
            summary['average_test_length'] = round(quality.get('average_test_length', 0), 1)
        
        return summary
    
    def save_analysis_results(self, result_dir, analysis_results, experiment_data):
        """Zapisuje wyniki analizy w różnych formatach"""
        # 1. Zapisz kompletne wyniki JSON
        analysis_file = result_dir / "analysis_results.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        # 2. Generuj CSV podobnie do manualnych analiz
        self.generate_csv_analysis(result_dir, analysis_results, experiment_data)
        
        # 3. Generuj markdown podsumowanie
        self.generate_markdown_summary(result_dir, analysis_results, experiment_data)
        
        logger.info(f"✓ Analysis results saved to {result_dir}")
    
    def generate_csv_analysis(self, result_dir, analysis_results, experiment_data):
        """Generuje CSV analizę w formacie podobnym do manualnego"""
        import csv
        
        # Przygotuj dane dla CSV
        model_name = experiment_data['model'].replace('.', '').replace(' ', '-')
        csv_file = result_dir / f"analiza-{model_name}.csv"
        
        # Pobierz pokryte scenariusze
        covered_scenarios = []
        if 'scenarios' in analysis_results and analysis_results['scenarios']:
            scenarios_data = analysis_results['scenarios'].get('covered_scenarios', {})
            
            # Mapuj scenariusze na format CSV (uproszczony)
            for method, count in scenarios_data.items():
                for i in range(count):
                    # Dodaj przykładowe scenariusze - to można rozszerzyć
                    covered_scenarios.append({
                        'Metoda': method.replace('_scenarios', ''),
                        'Typ': 'scenariusz' if 'corner' not in method else 'corner case',
                        'Opis scenariusza': f"Test {method} #{i+1}",
                        'Pokryty w testach': 1,
                        'Komentarz': ''
                    })
        
        # Zapisz CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Metoda', 'Typ', 'Opis scenariusza', 'Pokryty w testach', 'Komentarz'])
            writer.writeheader()
            writer.writerows(covered_scenarios)
        
        logger.info(f"✓ CSV analysis saved to {csv_file}")
    
    def generate_markdown_summary(self, result_dir, analysis_results, experiment_data):
        """Generuje markdown podsumowanie w formacie podobnym do manualnego"""
        summary = analysis_results.get('summary', {})
        model_name = experiment_data['model']
        strategy = experiment_data['strategy']
        context = experiment_data['context_type']
        
        md_file = result_dir / f"podsumowanie-{model_name.replace('.', '').replace(' ', '-')}.md"
        
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

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: {summary.get('total_defined_scenarios', 54)}

- Testy wygenerowane przez LLM: {summary.get('total_test_methods', 0)}
- Testy zakończone powodzeniem: {summary.get('tests_passed', 0)}
- Testy zakończone niepowodzeniem: {summary.get('tests_failed', 0)}

- Test success rate: {summary.get('test_success_rate', 0)}%
- Scenario coverage rate: {summary.get('scenario_coverage_rate', 0)}%

## Automatycznie wygenerowane przez LLM Testing Automation
- Response time: {summary.get('response_time', 0):.2f}s
- Generated at: {summary.get('timestamp', 'N/A')}

"""
        
        md_file.write_text(content, encoding='utf-8')
        logger.info(f"✓ Markdown summary saved to {md_file}")