"""
Klient dla Hugging Face Chat - darmowe modele LLM bez CAPTCHA
"""
import time
from base_llm_client import BaseLLMClient
from selenium.webdriver.common.keys import Keys
import logging

logger = logging.getLogger(__name__)

class HuggingFaceClient(BaseLLMClient):
    """Automatyzacja Hugging Face Chat"""
    
    def __init__(self, model_name="meta-llama/Llama-2-70b-chat-hf", headless=True):
        self.model_name = model_name
        self.base_url = "https://huggingface.co/chat"
        self.use_profile = False  # HF nie wymaga logowania
        super().__init__(headless)
    
    def get_selectors(self):
        """Selektory CSS dla Hugging Face Chat"""
        return {
            'input_box': 'textarea[placeholder*="Ask anything"]',
            'send_button': 'button[type="submit"]',
            'response_container': '.prose',
            'response_text': '.prose p',
            'model_selector': 'button[data-testid="model-selector"]',
            'loading_indicator': '.animate-pulse'
        }
    
    def login(self):
        """HuggingFace Chat nie wymaga logowania"""
        logger.info("Navigating to Hugging Face Chat...")
        self.driver.get(self.base_url)
        
        # Sprawdź czy strona się załadowała
        try:
            self.wait_for_element(self.get_selectors()['input_box'], timeout=10)
            logger.info("Hugging Face Chat loaded successfully!")
            return True
        except:
            logger.error("Failed to load Hugging Face Chat")
            return False
    
    def send_prompt(self, prompt_text, wait_for_completion=True):
        """Wysłanie promptu do Hugging Face"""
        selectors = self.get_selectors()
        
        try:
            # Znajdź pole tekstowe
            input_box = self.wait_for_element(selectors['input_box'])
            
            # Wyczyść i wpisz prompt
            input_box.clear()
            input_box.send_keys(prompt_text)
            
            # Wyślij prompt
            time.sleep(1)
            send_button = self.wait_for_clickable(selectors['send_button'])
            send_button.click()
            
            if wait_for_completion:
                return self.wait_for_response()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send prompt: {e}")
            return None
    
    def wait_for_response(self, max_wait_time=60):
        """Czeka na odpowiedź od Hugging Face"""
        selectors = self.get_selectors()
        start_time = time.time()
        
        time.sleep(3)  # Krótkie opóźnienie
        
        while time.time() - start_time < max_wait_time:
            try:
                # Sprawdź czy jest loading indicator
                loading_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, selectors['loading_indicator']
                )
                
                if not loading_elements:
                    # Pobierz odpowiedź
                    response_elements = self.driver.find_elements(
                        By.CSS_SELECTOR, selectors['response_text']
                    )
                    
                    if response_elements:
                        # Weź ostatnią odpowiedź
                        last_response = response_elements[-1]
                        response_text = last_response.text
                        
                        if response_text.strip():
                            self.response_time = time.time() - start_time
                            logger.info(f"Response received in {self.response_time:.2f}s")
                            return response_text
                
                time.sleep(2)
                
            except Exception as e:
                logger.debug(f"Waiting for response: {e}")
                time.sleep(2)
        
        logger.error("Response timeout")
        return None
    
    def extract_code_from_response(self, response_text):
        """Wyciąga kod Python z odpowiedzi"""
        import re
        
        # Szuka bloków kodu Python
        code_blocks = re.findall(r'```python\n(.*?)\n```', response_text, re.DOTALL)
        if code_blocks:
            return code_blocks[0]
        
        # Szuka bloków kodu bez specyfikacji języka
        code_blocks = re.findall(r'```\n(.*?)\n```', response_text, re.DOTALL)
        if code_blocks:
            for block in code_blocks:
                if any(keyword in block for keyword in ['import', 'def ', 'class ', 'unittest']):
                    return block
        
        return None