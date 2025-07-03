"""
Klient automatyzacji dla Claude (Anthropic)
"""
import time
from base_llm_client import BaseLLMClient
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)

class AnthropicClient(BaseLLMClient):
    """Automatyzacja Claude"""
    
    def __init__(self, model_name="claude-3.7-sonnet", headless=True, use_profile=True, attach_to_existing=False, debug_port=9222):
        self.model_name = model_name
        self.base_url = "https://claude.ai"
        self.use_profile = use_profile
        self.profile_name = "claude"
        self.attach_to_existing = attach_to_existing
        self.debug_port = debug_port
        super().__init__(headless)
    
    def get_selectors(self):
        """Selektory CSS dla Claude interface"""
        return {
            'input_box': 'div[contenteditable="true"]',
            'send_button': 'button[aria-label="Send Message"]',
            'response_container': '[data-testid="message"]',
            'response_text': '[data-testid="message"] .font-claude-message',
            'new_chat_button': 'button[aria-label="Start new chat"]',
            'loading_indicator': '[data-testid="typing-indicator"]',
            'code_block': 'pre code'
        }
    
    def login(self):
        """Logowanie do Claude"""
        logger.info("Navigating to Claude...")
        self.driver.get(self.base_url)
        
        # Sprawdź czy już zalogowany
        try:
            self.wait_for_element(self.get_selectors()['input_box'], timeout=5)
            logger.info("Already logged in!")
            return True
        except:
            logger.warning("Please log in manually and press Enter to continue...")
            input("Press Enter after login...")
            return True
    
    def send_prompt(self, prompt_text, wait_for_completion=True, skip_model_verification=False):
        """Wysłanie promptu do Claude"""
        selectors = self.get_selectors()
        start_time = time.time()  # Start timing
        
        try:
            # Znajdź pole tekstowe (contenteditable div)
            input_box = self.wait_for_element(selectors['input_box'])
            
            # Wyczyść i wpisz prompt
            input_box.clear()
            input_box.send_keys(prompt_text)
            
            # Znajdź i kliknij przycisk wysyłania
            time.sleep(1)
            send_button = self.wait_for_clickable(selectors['send_button'])
            send_button.click()
            logger.info("Prompt sent to Claude")
            
            # Verify message was sent by checking if send button is disabled/hidden
            time.sleep(1)
            try:
                is_still_clickable = send_button.is_enabled() and send_button.is_displayed()
                if is_still_clickable:
                    logger.warning("⚠️  Send button still clickable - message may not have been sent!")
                else:
                    logger.info("✅ Message sending verified - send button disabled/hidden")
            except:
                logger.info("✅ Send button state changed - likely sent")
            
            if wait_for_completion:
                response = self.wait_for_response()
                # Calculate and store response time
                self.last_response_time = time.time() - start_time
                logger.info(f"🕒 Total response time: {self.last_response_time:.2f}s")
                return response
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send prompt: {e}")
            self.last_response_time = 0
            return None
    
    def wait_for_response(self, max_wait_time=120):
        """Czeka na odpowiedź od Claude"""
        selectors = self.get_selectors()
        start_time = time.time()
        
        # Czekaj aż pojawi się wskaźnik pisania
        time.sleep(2)
        
        while time.time() - start_time < max_wait_time:
            try:
                # Sprawdź czy Claude wciąż pisze
                typing_indicators = self.driver.find_elements(
                    By.CSS_SELECTOR, selectors['loading_indicator']
                )
                
                if not typing_indicators:
                    # Brak wskaźnika pisania - prawdopodobnie skończone
                    # Pobierz ostatnią odpowiedź
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
        """Wyciąga kod Python z odpowiedzi Claude"""
        import re
        
        # Claude często umieszcza kod w blokach ```python
        code_blocks = re.findall(r'```python\n(.*?)\n```', response_text, re.DOTALL)
        if code_blocks:
            return code_blocks[0]
        
        # Alternatywnie sprawdź zwykłe bloki kodu
        code_blocks = re.findall(r'```\n(.*?)\n```', response_text, re.DOTALL)
        if code_blocks:
            for block in code_blocks:
                if any(keyword in block for keyword in ['import', 'def ', 'class ', 'unittest']):
                    return block
        
        return None
    
    def get_all_code_blocks(self):
        """Pobiera wszystkie bloki kodu z aktualnej konwersacji"""
        selectors = self.get_selectors()
        try:
            code_elements = self.driver.find_elements(
                By.CSS_SELECTOR, selectors['code_block']
            )
            return [elem.text for elem in code_elements]
        except Exception as e:
            logger.error(f"Failed to extract code blocks: {e}")
            return []