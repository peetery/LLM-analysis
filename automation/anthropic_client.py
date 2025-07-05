"""
Klient automatyzacji dla Claude (Anthropic) - przepisany na podstawie OpenAI client
"""
import time
from base_llm_client import BaseLLMClient
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)

class AnthropicClient(BaseLLMClient):
    """Automatyzacja Claude - przepisany na podstawie sprawdzonego OpenAI client"""

    def __init__(self, model_name="claude-3.7-sonnet", headless=True, use_profile=True, attach_to_existing=False, debug_port=9222):
        self.model_name = model_name
        self.base_url = "https://claude.ai/new"
        self.use_profile = use_profile
        self.profile_name = "claude"
        self.attach_to_existing = attach_to_existing
        self.debug_port = debug_port
        super().__init__(headless)

    def get_selectors(self):
        """CSS selectors for Claude interface - updated based on current structure"""
        return {
            # Input and sending
            'input_box': 'div[contenteditable="true"]',
            'input_box_alt': '[aria-label*="message"]',
            'send_button': 'button[aria-label*="Send"]',
            'send_button_alt': 'button[type="submit"]',

            # Response containers - focus on assistant messages
            'response_container': '[data-message-author-role="assistant"]',
            'response_text': '[data-message-author-role="assistant"]',
            'response_text_alt': 'div[role="article"]',

            # Chat management
            'new_chat_button': 'a[href*="/new"]',

            # Loading indicators
            'loading_indicator': '[data-testid="streaming"]',
            'stop_button': '[aria-label*="Stop"]'
        }

    def login(self):
        """Logowanie do Claude"""
        logger.info("Navigating to Claude...")

        # Sprawdź czy już zalogowany
        try:
            self.wait_for_element(self.get_selectors()['input_box'], timeout=5)
            logger.info("Already logged in!")
            return True
        except:
            logger.error("❌ NOT LOGGED IN! Please ensure you are logged into Claude before running automation.")
            logger.error("❌ Open Chrome, go to https://claude.ai, log in, then run automation.")
            return False

    def send_prompt(self, prompt_text, wait_for_completion=True, skip_model_verification=False):
        """Send prompt to Claude - based on OpenAI structure"""
        selectors = self.get_selectors()
        start_time = time.time()

        try:
            # Find text input
            input_box = self.wait_for_element(selectors['input_box'], timeout=10)
            if not input_box:
                # Try alternative selector
                input_box = self.wait_for_element(selectors['input_box_alt'], timeout=5)

            if not input_box:
                logger.error("Could not find input box")
                return None

            # Click to focus
            input_box.click()
            time.sleep(1)

            # Use JavaScript to set text content (like OpenAI)
            self.driver.execute_script("""
                var element = arguments[0];
                var text = arguments[1];
                
                // Clear any existing content
                element.innerHTML = '';
                element.textContent = '';
                
                // Set the text content (preserves newlines)
                element.textContent = text;
                
                // Trigger input events
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
                
                console.log('Text set in Claude:', text.length, 'characters');
            """, input_box, prompt_text)

            logger.info(f"Text set using JavaScript: {len(prompt_text)} characters")
            time.sleep(2)

            # Send the message
            send_button = None
            send_selectors = [selectors['send_button'], selectors['send_button_alt']]

            for selector in send_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in buttons:
                        if button.is_enabled() and button.is_displayed():
                            send_button = button
                            break
                    if send_button:
                        break
                except:
                    continue

            if send_button:
                try:
                    send_button.click()
                    logger.info("Prompt sent via button click")
                except:
                    # JavaScript click fallback
                    self.driver.execute_script("arguments[0].click();", send_button)
                    logger.info("Prompt sent via JavaScript click")
            else:
                # Fallback: Use Enter key
                input_box.send_keys(Keys.RETURN)
                logger.info("Prompt sent via Enter key")

            if wait_for_completion:
                response = self.wait_for_response()
                self.last_response_time = time.time() - start_time
                logger.info(f"🕒 Total response time: {self.last_response_time:.2f}s")
                return response

            return True

        except Exception as e:
            logger.error(f"Failed to send prompt: {e}")
            self.last_response_time = 0
            return None

    def wait_for_response(self, max_wait_time=120):
        """Wait for Claude response - based on OpenAI logic"""
        selectors = self.get_selectors()
        start_time = time.time()

        # CRITICAL: First check if generation actually started
        time.sleep(2)
        initial_send_buttons = self.driver.find_elements(By.CSS_SELECTOR, selectors['send_button'])
        if initial_send_buttons:
            initial_send_button = initial_send_buttons[0]
            is_still_enabled = initial_send_button.is_enabled() and initial_send_button.is_displayed()
            if is_still_enabled:
                logger.error("❌ CRITICAL: Send button still enabled after 2s - message was NOT sent!")
                return None

        logger.info("✅ Send button disabled - generation started")

        # CLAUDE FIX: Add temporary text to enable Send button detection during generation
        # This allows us to detect when generation finishes (Send button becomes enabled)
        temp_text_added = False
        try:
            input_box = self.driver.find_element(By.CSS_SELECTOR, selectors['input_box'])
            if input_box:
                # Add a single space as temporary text
                self.driver.execute_script("""
                    var element = arguments[0];
                    element.textContent = ' ';
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                """, input_box)
                temp_text_added = True
                logger.debug("Added temporary text for Send button detection")
        except:
            logger.debug("Could not add temporary text - will rely on other indicators")

        # Wait for generation to continue
        time.sleep(3)

        # Track the last response length to detect when generation stops
        last_response_length = 0
        stable_count = 0
        min_response_length = 200

        while time.time() - start_time < max_wait_time:
            try:
                # Primary check: look for stop button (indicates generation)
                stop_buttons = self.driver.find_elements(By.CSS_SELECTOR, selectors['stop_button'])
                if stop_buttons and any(btn.is_displayed() for btn in stop_buttons):
                    logger.debug("Stop button visible - still generating...")
                    time.sleep(3)
                    continue

                # Check loading indicators
                loading_indicators = self.driver.find_elements(By.CSS_SELECTOR, selectors['loading_indicator'])
                if loading_indicators and any(elem.is_displayed() for elem in loading_indicators):
                    logger.debug("Loading indicator visible - still generating...")
                    time.sleep(3)
                    continue

                # Secondary check: send button state
                send_buttons = self.driver.find_elements(By.CSS_SELECTOR, selectors['send_button'])
                if send_buttons:
                    send_button = send_buttons[0]
                    is_disabled = send_button.get_attribute('disabled') or not send_button.is_enabled()

                    if not is_disabled:
                        # Send button is ENABLED - this means NO generation is happening
                        logger.debug("Send button is enabled - generation finished")
                    else:
                        logger.debug("Send button disabled - still generating...")
                        time.sleep(3)
                        continue

                # Get response - multiple approaches like OpenAI
                response_text = None

                # Try main response selectors
                response_selectors = [
                    selectors['response_text'],
                    selectors['response_text_alt'],
                    '[data-message-author-role="assistant"] .markdown',
                    '[data-message-author-role="assistant"] div',
                    'div[role="article"]',
                    '.message-content'
                ]

                for selector in response_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            last_element = elements[-1]
                            text = last_element.text.strip()
                            # Skip our prompt and look for actual response
                            if (text and len(text) > len(response_text or "") and
                                'Generate a complete Python unit test suite' not in text and
                                len(text) > 50):
                                response_text = text
                                logger.debug(f"✓ Found response via {selector}: {len(text)} chars")
                                break
                    except:
                        continue

                # Fallback: Use JavaScript to find response (like OpenAI)
                if not response_text:
                    logger.debug("No response found via selectors, trying JavaScript...")
                    try:
                        js_response = self.driver.execute_script("""
                            // Search for Claude's response - look for test code specifically
                            // FIXED: Better detection to avoid cutting off first line
                            var keywords = ['import unittest', 'class Test', 'def test_', 'unittest.TestCase', 'import ', 'from ', 'class ', 'def '];
                            var allElements = Array.from(document.querySelectorAll('*'));
                            var bestMatch = '';
                            var bestScore = 0;
                            
                            for (var elem of allElements) {
                                var text = elem.textContent || elem.innerText || '';
                                
                                // Skip our prompt and look for substantial test code
                                if (text.length > 500 && 
                                    !text.includes('Generate a complete Python unit test suite') &&
                                    !text.includes('Write your prompt to Claude') &&
                                    !text.includes('intercom-lightweight-app')) {  // Skip UI elements
                                    
                                    var score = 0;
                                    for (var keyword of keywords) {
                                        if (text.includes(keyword)) {
                                            score += keyword.length;
                                        }
                                    }
                                    
                                    // Prefer responses that start with import (complete code)
                                    if (text.trimStart().startsWith('import') || text.trimStart().startsWith('from')) {
                                        score += 100; // Bonus for complete code
                                    }
                                    
                                    if (score > bestScore && text.length < 50000) {  // Avoid huge page content
                                        bestScore = score;
                                        bestMatch = text;
                                    }
                                }
                            }
                            
                            return bestMatch || null;
                        """)

                        if js_response and len(js_response) > len(response_text or ""):
                            response_text = js_response
                            logger.debug(f"✓ Found response via JavaScript: {len(js_response)} chars")
                    except Exception as e:
                        logger.debug(f"JavaScript fallback failed: {e}")

                if response_text:
                    current_length = len(response_text)

                    # For large responses, likely complete
                    if current_length > 3000 and ('import unittest' in response_text or 'class Test' in response_text):
                        logger.info(f"Substantial code response detected ({current_length} chars)")
                        self.response_time = time.time() - start_time
                        return response_text

                    logger.debug(f"Current response length: {current_length} chars")

                    # Standard stability check (like OpenAI)
                    if current_length < min_response_length:
                        if current_length == last_response_length:
                            stable_count += 1
                            if stable_count >= 5:
                                logger.warning(f"Short response detected: {current_length} chars")
                                self.response_time = time.time() - start_time
                                return response_text
                        else:
                            stable_count = 0
                            last_response_length = current_length
                    else:
                        if current_length == last_response_length:
                            stable_count += 1
                            if stable_count >= 3:  # Stable for 3 checks
                                self.response_time = time.time() - start_time
                                logger.info(f"Response received in {self.response_time:.2f}s ({len(response_text)} chars)")

                                # Clean up temporary text if added
                                if temp_text_added:
                                    try:
                                        self.driver.execute_script("""
                                            var element = arguments[0];
                                            element.textContent = '';
                                        """, input_box)
                                        logger.debug("Cleaned up temporary text")
                                    except:
                                        pass

                                return response_text
                        else:
                            stable_count = 0
                            last_response_length = current_length

                time.sleep(3)

            except Exception as e:
                logger.debug(f"Waiting for response: {e}")
                time.sleep(3)

        logger.error("Response timeout")
        return None

    def start_new_chat(self):
        """Start new chat"""
        try:
            current_url = self.driver.current_url
            if "/new" not in current_url:
                self.driver.get("https://claude.ai/new")
                logger.info("New chat started by navigating to /new")
                time.sleep(3)
                return True
            else:
                logger.debug("Already on /new chat page")
                return True
        except Exception as e:
            logger.error(f"Failed to start new chat: {e}")
            return False

    def extract_code_from_response(self, response_text):
        """Extract Python code from Claude's response"""
        import re

        # Claude often puts code in ```python blocks
        code_blocks = re.findall(r'```python\n(.*?)\n```', response_text, re.DOTALL)
        if code_blocks:
            return code_blocks[0]

        # Alternative: check regular code blocks
        code_blocks = re.findall(r'```\n(.*?)\n```', response_text, re.DOTALL)
        if code_blocks:
            for block in code_blocks:
                if 'import' in block or 'class' in block or 'def' in block:
                    return block

        # If no code blocks found, return the whole response if it looks like code
        if ('import' in response_text and 'class' in response_text and
            'def' in response_text and len(response_text) > 100):
            return response_text

        return None

    def select_model(self):
        """Skip model selection - user selects manually"""
        logger.info("Skipping model selection - user will select manually")
        return True