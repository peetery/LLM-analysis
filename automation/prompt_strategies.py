"""
Strategie promptowania: Simple i Chain-of-Thought
"""
import time
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class PromptStrategy:
    """Bazowa klasa strategii promptowania"""
    
    def __init__(self, base_path=None):
        if base_path is None:
            # Znajdź katalog prompts_results względem lokalizacji skryptu
            current_file = Path(__file__).parent
            self.base_path = current_file.parent / "prompts_results"
            
            # Debug: sprawdź czy ścieżka jest prawidłowa
            if not self.base_path.exists():
                logger.warning(f"Base path {self.base_path} doesn't exist, trying alternative paths")
                # Spróbuj inne ścieżki
                alternatives = [
                    Path.cwd().parent / "prompts_results",  # parent of current working dir
                    Path.cwd() / ".." / "prompts_results",  # relative to cwd
                    current_file.parent.parent / "prompts_results"  # parent.parent
                ]
                
                for alt_path in alternatives:
                    if alt_path.exists():
                        self.base_path = alt_path.resolve()
                        logger.info(f"Found prompts_results at: {self.base_path}")
                        break
                else:
                    logger.error(f"Could not find prompts_results directory in any of: {[str(p) for p in alternatives]}")
        else:
            self.base_path = Path(base_path)
        self.load_prompts()
    
    def load_prompts(self):
        """Load prompt templates from files - lazy loading"""
        self.prompts = {}
        
        # Check if directory exists
        if not self.base_path.exists():
            logger.warning(f"Directory {self.base_path} does not exist!")
            return
        
        logger.info(f"Prompt base path: {self.base_path}")
    
    def load_specific_prompt(self, strategy, context):
        """Load only the specific prompt needed"""
        if strategy == "simple_prompting":
            key = context
            prompt_file = self.base_path / "simple_prompting" / context / "prompt.txt"
        else:  # chain_of_thought_prompting
            key = f"cot_{context}"
            prompt_file = self.base_path / "chain_of_thought_prompting" / context / "prompt.txt"
        
        logger.info(f"Looking for prompt: {strategy}/{context} at {prompt_file}")
        logger.info(f"Base path: {self.base_path}")
        logger.info(f"File exists: {prompt_file.exists()}")
        
        if key not in self.prompts:
            if prompt_file.exists():
                try:
                    self.prompts[key] = prompt_file.read_text(encoding='utf-8')
                    logger.info(f"✓ Loaded prompt: {strategy}/{context} ({len(self.prompts[key])} chars)")
                except Exception as e:
                    logger.error(f"✗ Error reading prompt file {prompt_file}: {e}")
                    return None
            else:
                logger.error(f"✗ Prompt not found: {prompt_file}")
                # List available files for debugging
                if prompt_file.parent.exists():
                    available_files = list(prompt_file.parent.iterdir())
                    logger.error(f"Available files in {prompt_file.parent}: {[f.name for f in available_files]}")
                return None
        
        return self.prompts.get(key)
    
    def parse_cot_content(self, content):
        """Parse CoT content into steps"""
        steps = {}
        parts = content.split('\n\n')
        
        current_step = None
        current_content = []
        
        for part in parts:
            part = part.strip()
            if part.startswith('1)'):
                if current_step:
                    steps[current_step] = '\n\n'.join(current_content)
                current_step = 'step1'
                current_content = [part[2:].strip()]
            elif part.startswith('2)'):
                if current_step:
                    steps[current_step] = '\n\n'.join(current_content)
                current_step = 'step2'
                current_content = [part[2:].strip()]
            elif part.startswith('3)'):
                if current_step:
                    steps[current_step] = '\n\n'.join(current_content)
                current_step = 'step3'
                current_content = [part[2:].strip()]
            elif current_step:
                current_content.append(part)
        
        # Add last step
        if current_step and current_content:
            steps[current_step] = '\n\n'.join(current_content)
        
        return steps
    
    def get_context_content(self, context_type):
        """Pobiera zawartość kontekstu na podstawie typu"""
        if context_type == "interface":
            return self.get_interface_only()
        elif context_type == "interface_docstring":
            return self.get_interface_with_docstrings()
        elif context_type == "full_context":
            return self.get_full_context()
        else:
            raise ValueError(f"Unknown context type: {context_type}")
    
    def get_interface_only(self):
        """Zwraca tylko sygnatury metod"""
        return '''class OrderCalculator:
    def __init__(self, tax_rate=0.08, shipping_cost=5.0):
        pass
    
    def calculate_subtotal(self, items):
        pass
    
    def calculate_tax(self, subtotal):
        pass
    
    def calculate_shipping(self, items, subtotal):
        pass
    
    def apply_discount(self, subtotal, discount_code=None):
        pass
    
    def calculate_total(self, items, discount_code=None):
        pass'''
    
    def get_interface_with_docstrings(self):
        """Zwraca sygnatury z docstringami"""
        order_calc_path = Path("order_calculator.py")
        if order_calc_path.exists():
            content = order_calc_path.read_text()
            # Wyciąga tylko sygnatury i docstringi
            # Implementacja może być bardziej zaawansowana
            return content
        return self.get_interface_only()
    
    def get_full_context(self):
        """Zwraca pełny kod źródłowy"""
        order_calc_path = Path("order_calculator.py")
        if order_calc_path.exists():
            return order_calc_path.read_text()
        return ""


class SimplePrompting(PromptStrategy):
    """Strategia prostego promptowania"""
    
    def execute(self, llm_client, context_type):
        """Execute simple prompting strategy"""
        logger.info(f"Executing simple prompting strategy for {context_type}")
        
        # Load only the specific prompt needed
        final_prompt = self.load_specific_prompt("simple_prompting", context_type)
        if not final_prompt:
            logger.error(f"No prompt template found for simple_prompting/{context_type}")
            return None
        
        # Wyślij prompt - pomiar czasu wewnątrz send_prompt
        response = llm_client.send_prompt(final_prompt)
        # Pobierz czas odpowiedzi z klienta (jeśli dostępny)
        response_time = getattr(llm_client, 'last_response_time', 0)
        
        if response:
            logger.info(f"Simple prompting completed in {response_time:.2f}s")
            return {
                'response': response,
                'response_time': response_time,
                'strategy': 'simple_prompting',
                'context_type': context_type,
                'prompt': final_prompt
            }
        
        return None


class ChainOfThoughtPrompting(PromptStrategy):
    """Strategia Chain-of-Thought promptowania (3 kroki)"""
    
    def __init__(self, base_path=None):
        super().__init__(base_path)
        self.cot_prompts = self.parse_cot_prompts()
    
    def parse_cot_prompts(self):
        """Parsuje prompty Chain-of-Thought z plików - używa lazy loading"""
        # Nie ładujemy wszystkich promptów teraz, tylko sprawdzamy czy istnieją
        cot_prompts = {}
        
        for context in ['interface', 'interface_docstring', 'full_context']:
            prompt_file = self.base_path / "chain_of_thought_prompting" / context / "prompt.txt"
            if prompt_file.exists():
                logger.info(f"✓ Found CoT prompt file for {context}: {prompt_file}")
                cot_prompts[context] = True  # Mark as available
            else:
                logger.warning(f"✗ Missing CoT prompt file for {context}: {prompt_file}")
        
        return cot_prompts
    
    def execute(self, llm_client, context_type):
        """Execute Chain-of-Thought strategy (3 steps)"""
        logger.info(f"Executing chain-of-thought prompting for {context_type}")
        
        # Load only the specific CoT prompt needed
        cot_content = self.load_specific_prompt("chain_of_thought_prompting", context_type)
        if not cot_content:
            logger.error(f"No CoT prompt found for {context_type}")
            return None
        
        # Parse the CoT steps from content
        steps = self.parse_cot_content(cot_content)
        if not steps:
            logger.error(f"Could not parse CoT steps from prompt")
            return None
        total_time = 0
        responses = []
        
        # Krok 1: Analiza
        logger.info("Step 1: Code analysis")
        prompt1 = steps.get('step1', '')
        if not prompt1:
            logger.error("No step1 prompt found")
            return None
        
        response1 = llm_client.send_prompt(prompt1)
        step1_time = getattr(llm_client, 'last_response_time', 0)
        total_time += step1_time
        
        if not response1:
            logger.error("Failed at step 1")
            return None
        
        responses.append({
            'step': 1,
            'prompt': prompt1,
            'response': response1,
            'response_time': step1_time
        })
        
        # Krótka przerwa między krokami
        time.sleep(2)
        
        # Krok 2: Strategia
        logger.info("Step 2: Test strategy")
        prompt2 = steps.get('step2', '')
        if not prompt2:
            logger.error("No step2 prompt found")
            return None
            
        response2 = llm_client.send_prompt(prompt2)
        step2_time = getattr(llm_client, 'last_response_time', 0)
        total_time += step2_time
        
        if not response2:
            logger.error("Failed at step 2")
            return None
        
        responses.append({
            'step': 2,
            'prompt': prompt2,
            'response': response2,
            'response_time': step2_time
        })
        
        time.sleep(2)
        
        # Krok 3: Implementacja
        logger.info("Step 3: Code generation")
        prompt3 = steps.get('step3', '')
        if not prompt3:
            logger.error("No step3 prompt found")
            return None
            
        response3 = llm_client.send_prompt(prompt3)
        step3_time = getattr(llm_client, 'last_response_time', 0)
        total_time += step3_time
        
        if not response3:
            logger.error("Failed at step 3")
            return None
        
        responses.append({
            'step': 3,
            'prompt': prompt3,
            'response': response3,
            'response_time': step3_time
        })
        
        logger.info(f"Chain-of-thought completed in {total_time:.2f}s")
        
        return {
            'responses': responses,
            'final_response': response3,  # Kod testów z ostatniego kroku
            'total_response_time': total_time,
            'strategy': 'chain_of_thought_prompting',
            'context_type': context_type
        }