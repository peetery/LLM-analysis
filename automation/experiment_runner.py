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
                # Auto-navigate to the correct model URL
                model_urls = {
                    'gpt-4.5': 'https://chatgpt.com/',
                    'gpt-o3': 'https://chatgpt.com/',
                    'gpt-o4-mini-high': 'https://chatgpt.com/',
                    'claude-3.7-sonnet': 'https://claude.ai/',
                    'deepseek': 'https://chat.deepseek.com/',
                    'gemini-2.5-pro': 'https://gemini.google.com/'
                }
                
                target_url = model_urls.get(model_name, 'https://google.com')
                logger.info(f"Navigating to {target_url}")
                llm_client.driver.get(target_url)
                time.sleep(3)
                
                # Login
                if not llm_client.login():
                    logger.error("Failed to login")
                    return None
                
                # Select specific model if available
                if hasattr(llm_client, 'select_model'):
                    llm_client.select_model(model_name)
                
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
                
                # Zapisz wyniki
                experiment_results = self.save_experiment_results(
                    result_dir, strategy_result, model_name, strategy_name, context_type
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
        """Uruchamia analizę testów"""
        tests_file = Path(experiment_data['test_file'])
        
        if not tests_file.exists():
            logger.error(f"Test file not found: {tests_file}")
            return None
        
        analysis_results = {}
        
        # 1. Test kompilacji
        compilation_success = self.test_compilation(tests_file)
        analysis_results['compilation_success'] = compilation_success
        
        if not compilation_success:
            logger.error("Tests do not compile")
            return analysis_results
        
        # 2. Uruchom coverage
        coverage_results = self.run_coverage_analysis(result_dir, tests_file)
        analysis_results['coverage'] = coverage_results
        
        # 3. Uruchom mutation testing
        mutation_results = self.run_mutation_testing(result_dir)
        analysis_results['mutation'] = mutation_results
        
        # 4. Analiza scenariuszy
        scenario_analysis = self.analyze_test_scenarios(tests_file)
        analysis_results['scenarios'] = scenario_analysis
        
        # Zapisz wyniki analizy
        analysis_file = result_dir / "analysis_results.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        return analysis_results
    
    def test_compilation(self, tests_file):
        """Testuje czy testy się kompilują"""
        try:
            result = subprocess.run(
                ['python', '-m', 'py_compile', str(tests_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Compilation test failed: {e}")
            return False
    
    def run_coverage_analysis(self, result_dir, tests_file):
        """Uruchamia analizę pokrycia kodu"""
        try:
            # Uruchom testy z coverage
            cmd = [
                'python', '-m', 'coverage', 'run', 
                '--source=.', '-m', 'unittest', 
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
        """Parsuje wyniki coverage"""
        lines = coverage_output.strip().split('\n')
        
        for line in lines:
            if 'order_calculator.py' in line:
                parts = line.split()
                if len(parts) >= 4:
                    return {
                        'statements': int(parts[1]),
                        'missing': int(parts[2]),
                        'coverage_percent': int(parts[3].replace('%', ''))
                    }
        
        return None
    
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
        """Parsuje wyniki mutmut"""
        # Podstawowe parsowanie - może być rozszerzone
        stats = {
            'total_mutants': 0,
            'killed': 0,
            'survived': 0,
            'timeout': 0,
            'mutation_score': 0
        }
        
        for line in mutmut_output.split('\n'):
            if 'Total:' in line and 'killed:' in line:
                # Próba wyciągnięcia statystyk
                pass
        
        return stats
    
    def analyze_test_scenarios(self, tests_file):
        """Analizuje pokrycie scenariuszy testowych"""
        # Załaduj scenariusze z pliku
        scenarios_file = Path("scenariusze_testowe.md")
        if not scenarios_file.exists():
            return None
        
        # Analiza pokrycia scenariuszy - uproszczona wersja
        test_content = tests_file.read_text()
        
        # Zlicz testy
        test_methods = test_content.count('def test_')
        
        return {
            'total_test_methods': test_methods,
            'estimated_scenario_coverage': min(test_methods, 54)  # Max 54 scenariusze
        }
    
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