"""
Klient automatyzacji dla ChatGPT (OpenAI)
"""
import time
from base_llm_client import BaseLLMClient
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)

class OpenAIClient(BaseLLMClient):
    """Automatyzacja ChatGPT"""
    
    def __init__(self, model_name="gpt-4", headless=True, use_profile=True, attach_to_existing=False, debug_port=9222):
        self.model_name = model_name
        self.base_url = "https://chat.openai.com"
        self.use_profile = use_profile
        self.profile_name = "chatgpt"
        self.attach_to_existing = attach_to_existing
        self.debug_port = debug_port
        super().__init__(headless)
    
    def get_selectors(self):
        """CSS selectors for ChatGPT interface"""
        return {
            'input_box': '#prompt-textarea',  # Updated to match working selector
            'send_button': 'button[data-testid="send-button"]',
            'response_container': '[data-message-author-role="assistant"]',
            'response_text': '[data-message-author-role="assistant"] .markdown',
            'new_chat_button': 'a[href="/"]',
            'model_selector': '[data-testid="model-switcher"]',
            'loading_indicator': '.text-token-text-secondary'
        }
    
    def login(self):
        """Logowanie do ChatGPT - wymaga manualnego zalogowania"""
        logger.info("Navigating to ChatGPT...")
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
    
    def send_prompt(self, prompt_text, wait_for_completion=True):
        """Send prompt to ChatGPT"""
        selectors = self.get_selectors()
        
        try:
            # Find text input (ProseMirror contenteditable div)
            input_box = self.wait_for_element(selectors['input_box'])
            
            # Click to focus
            input_box.click()
            time.sleep(1)
            
            # Use JavaScript to set text content (preserves newlines)
            self.driver.execute_script("""
                var element = arguments[0];
                var text = arguments[1];
                
                // Clear any existing content
                element.innerHTML = '';
                element.textContent = '';
                
                // Set the text content (preserves newlines)
                element.textContent = text;
                
                // Trigger input event for ProseMirror
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
                
                console.log('Text set in ProseMirror:', text.length, 'characters');
            """, input_box, prompt_text)
            
            logger.info(f"Text set using JavaScript textContent: {len(prompt_text)} characters")
            
            # Wait for UI to process
            time.sleep(2)
            
            # Verify text was set correctly
            current_text = self.driver.execute_script("return arguments[0].textContent;", input_box)
            if len(current_text) < len(prompt_text) * 0.9:
                logger.warning(f"Text may not be fully set. Expected: {len(prompt_text)}, Got: {len(current_text)}")
            else:
                logger.info(f"✓ Text verified: {len(current_text)} characters")
            
            # Find and click send button
            send_selectors = [
                'button[data-testid="send-button"]',
                'button[aria-label*="Send"]',
                'button svg',
                '[data-testid="send-button"]'
            ]
            
            send_button = None
            for selector in send_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if buttons:
                        send_button = buttons[0]
                        logger.info(f"Found send button: {selector}")
                        break
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
            
            if send_button:
                send_button.click()
                logger.info("Prompt sent via send button click")
                
                if wait_for_completion:
                    return self.wait_for_response()
                return True
            else:
                logger.error("Send button not found")
                return None
            
        except Exception as e:
            logger.error(f"Failed to send prompt: {e}")
            return None
    
    def wait_for_response(self, max_wait_time=180):
        """Wait for ChatGPT response"""
        selectors = self.get_selectors()
        start_time = time.time()
        
        logger.info("Waiting for ChatGPT response...")
        
        # Wait for generation to start
        time.sleep(3)
        
        # Track the last response length to detect when generation stops
        last_response_length = 0
        stable_count = 0
        min_response_length = 200  # Minimum expected response length
        
        while time.time() - start_time < max_wait_time:
            try:
                # Primary check: look for stop button (indicates generation)
                stop_buttons = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="stop-button"]')
                if stop_buttons and any(btn.is_displayed() for btn in stop_buttons):
                    logger.debug("Stop button visible - still generating...")
                    time.sleep(3)
                    continue
                
                # Secondary check: send button disabled
                send_buttons = self.driver.find_elements(By.CSS_SELECTOR, selectors['send_button'])
                if send_buttons:
                    send_button = send_buttons[0]
                    is_disabled = send_button.get_attribute('disabled') or not send_button.is_enabled()
                    
                    if is_disabled:
                        logger.debug("Send button disabled - still generating...")
                        time.sleep(3)
                        continue
                
                # Get response with multiple selectors
                response_text = None
                response_selectors = [
                    '[data-message-author-role="assistant"]',
                    '[data-testid="conversation-turn"]:last-child [data-message-author-role="assistant"]',
                    '.markdown',
                    '[role="article"]'
                ]
                
                for selector in response_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            last_element = elements[-1]
                            text = last_element.text.strip()
                            if text and len(text) > len(response_text or ""):
                                response_text = text
                    except:
                        continue
                
                if response_text:
                    current_length = len(response_text)
                    logger.debug(f"Current response length: {current_length} chars")
                    
                    # For short responses, wait longer to ensure completion
                    if current_length < min_response_length:
                        if current_length == last_response_length:
                            stable_count += 1
                            if stable_count >= 5:  # Wait longer for short responses
                                logger.warning(f"Short response detected: {current_length} chars")
                                self.response_time = time.time() - start_time
                                return response_text
                        else:
                            stable_count = 0
                            last_response_length = current_length
                    else:
                        # For normal length responses, standard stability check
                        if current_length == last_response_length:
                            stable_count += 1
                            if stable_count >= 3:  # Stable for 3 checks
                                self.response_time = time.time() - start_time
                                logger.info(f"Response received in {self.response_time:.2f}s ({len(response_text)} chars)")
                                return response_text
                        else:
                            stable_count = 0
                            last_response_length = current_length
                
                time.sleep(2)
                
            except Exception as e:
                logger.debug(f"Waiting for response: {e}")
                time.sleep(2)
        
        logger.error("Response timeout")
        return None
    
    def start_new_chat(self):
        """Start new chat"""
        # Try multiple selectors for new chat
        new_chat_selectors = [
            'button[aria-label="New chat"]',
            'a[href="/"]',
            'button:has(svg)',
            '[data-testid="new-chat-button"]',
            'nav a[href="/"]'
        ]
        
        for selector in new_chat_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    try:
                        if element.is_displayed() and element.is_enabled():
                            element.click()
                            time.sleep(2)
                            logger.info(f"New chat started with selector: {selector}")
                            return True
                    except:
                        continue
            except:
                continue
        
        # If clicking doesn't work, navigate to home
        try:
            current_url = self.driver.current_url
            if "/c/" in current_url:  # We're in a conversation
                self.driver.get("https://chatgpt.com/")
                time.sleep(3)
                logger.info("Started new chat by navigating to home")
                return True
        except:
            pass
            
        logger.warning("Could not start new chat")
        return False
    
    def select_model(self, model_name):
        """Select specific GPT model if available"""
        try:
            # Try to find and click model selector
            model_selectors = [
                '[data-testid="model-switcher"]',
                'button[aria-haspopup="menu"]',
                'button:has(span:contains("GPT"))',
                '.model-selector'
            ]
            
            for selector in model_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            element.click()
                            time.sleep(2)
                            
                            # Look for specific model option
                            model_options = self.driver.find_elements(By.CSS_SELECTOR, '[role="menuitem"], [role="option"]')
                            for option in model_options:
                                if model_name.lower() in option.text.lower() or "gpt-4" in option.text.lower():
                                    option.click()
                                    time.sleep(1)
                                    logger.info(f"Selected model: {model_name}")
                                    return True
                            break
                except:
                    continue
            
            logger.info(f"Could not select specific model {model_name}, using default")
            return True  # Continue anyway
            
        except Exception as e:
            logger.warning(f"Model selection failed: {e}")
            return True  # Continue anyway
    
    def extract_code_from_response(self, response_text):
        """Extract Python code from response, cleaning ChatGPT UI artifacts"""
        import re
        
        def clean_code_block(code):
            """Clean ChatGPT UI artifacts from code"""
            lines = code.split('\n')
            cleaned_lines = []
            
            for line in lines:
                original_line = line
                line_stripped = line.strip()
                
                # Skip ChatGPT UI elements (more comprehensive)
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
                    
                cleaned_lines.append(original_line)  # Keep original indentation
            
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
                if any(keyword in cleaned_block for keyword in ['import', 'def ', 'class ', 'unittest']):
                    return cleaned_block
        
        # Last resort: find code starting with import or class
        lines = response_text.split('\n')
        code_start = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            if (line.startswith('import ') or 
                line.startswith('from ') or 
                (line.startswith('class ') and 'Test' in line)):
                code_start = i
                break
        
        if code_start is not None:
            code_lines = lines[code_start:]
            # Find logical end of code
            code_end = len(code_lines)
            for i, line in enumerate(code_lines):
                if (line.strip() and 
                    not line.startswith(' ') and 
                    not line.startswith('\t') and
                    not any(keyword in line for keyword in ['import', 'from', 'class', 'def', 'if __name__'])):
                    if i > 10:  # Only if we have substantial code
                        code_end = i
                        break
            
            code = '\n'.join(code_lines[:code_end])
            return clean_code_block(code)
        
        return None