"""
Klient automatyzacji dla Deepseek
"""
import time
from base_llm_client import BaseLLMClient
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)

class DeepseekClient(BaseLLMClient):
    """Automatyzacja Deepseek"""
    
    def __init__(self, model_name="deepseek", headless=True, use_profile=True):
        self.model_name = model_name
        self.base_url = "https://chat.deepseek.com"
        self.use_profile = use_profile
        self.profile_name = "deepseek"
        super().__init__(headless)
    
    def get_selectors(self):
        """Selektory CSS dla Deepseek interface"""
        return {
            'input_box': 'textarea[placeholder*="Ask me anything"]',
            'send_button': 'button[type="submit"]',
            'response_container': '.message-content',
            'response_text': '.message-content .markdown',
            'new_chat_button': 'button[aria-label="New chat"]',
            'loading_indicator': '.typing-indicator',
            'code_block': 'pre code'
        }
    
    def login(self):
        """Logowanie do Deepseek"""
        logger.info("Navigating to Deepseek...")
        self.driver.get(self.base_url)
        
        # Sprawdź czy już zalogowany
        try:
            self.wait_for_element(self.get_selectors()['input_box'], timeout=10)
            logger.info("Already logged in or no login required!")
            return True
        except:
            logger.warning("Login may be required - check manually")
            input("Login if needed and press Enter...")
            return True
    
    def send_prompt(self, prompt_text, wait_for_completion=True):
        """Wysłanie promptu do Deepseek"""
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
    
    def wait_for_response(self, max_wait_time=120):
        """Czeka na odpowiedź od Deepseek"""
        selectors = self.get_selectors()
        start_time = time.time()
        
        time.sleep(3)
        
        while time.time() - start_time < max_wait_time:
            try:
                # Sprawdź czy wciąż generuje
                typing_indicators = self.driver.find_elements(
                    By.CSS_SELECTOR, selectors['loading_indicator']
                )
                
                if not typing_indicators:
                    # Pobierz ostatnią odpowiedź
                    response_elements = self.driver.find_elements(
                        By.CSS_SELECTOR, selectors['response_text']
                    )
                    
                    if response_elements:
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
    
    def start_new_chat(self):
        """Rozpoczyna nowy chat"""
        selectors = self.get_selectors()
        try:
            if self.safe_click(selectors['new_chat_button']):
                time.sleep(2)
                return True
        except:
            pass
        return False
    
    def extract_code_from_response(self, response_text):
        """Wyciąga kod Python z odpowiedzi Deepseek"""
        import re
        
        code_blocks = re.findall(r'```python\n(.*?)\n```', response_text, re.DOTALL)
        if code_blocks:
            return code_blocks[0]
        
        code_blocks = re.findall(r'```\n(.*?)\n```', response_text, re.DOTALL)
        if code_blocks:
            for block in code_blocks:
                if any(keyword in block for keyword in ['import', 'def ', 'class ', 'unittest']):
                    return block
        
        return None