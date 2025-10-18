"""
Klient automatyzacji dla Deepseek - przepisany na podstawie OpenAI client
"""
import time
from base_llm_client import BaseLLMClient
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)

class DeepseekClient(BaseLLMClient):

    def __init__(self, model_name="deepseek", headless=True, use_profile=True, attach_to_existing=False, debug_port=9222):
        self.model_name = model_name
        self.base_url = "https://chat.deepseek.com"
        self.use_profile = use_profile
        self.profile_name = "deepseek"
        self.attach_to_existing = attach_to_existing
        self.debug_port = debug_port
        super().__init__(headless)

    def get_selectors(self):
        return {
            'input_box': 'div[contenteditable="true"]',
            'input_box_alt': 'textarea',
            'input_box_alt2': '[placeholder*="message"]',
            'input_box_alt3': '[role="textbox"]',
            'send_button': 'button[type="submit"]',
            'send_button_alt': 'button[aria-label*="Send"]',
            'send_button_alt2': 'svg[data-icon="send"]',

            'response_container': '.message-item',
            'response_text': '.message-content',
            'response_text_alt': '[data-role="assistant"]',
            'response_text_alt2': '.assistant-message',
            'response_text_alt3': '.response-content',

            'new_chat_button': '[data-testid="new-chat"]',
            'new_chat_button_alt': 'button[aria-label*="New"]',
            'new_chat_button_alt2': '.new-chat-button',

            'loading_indicator': '.loading',
            'loading_indicator_alt': '.typing-indicator',
            'stop_button': '[aria-label*="Stop"]',
            'stop_button_alt': 'button[data-testid="stop"]',
            'stop_button_alt2': '[aria-label*="stop" i]',
            'stop_button_alt3': 'button[aria-label*="stop" i]',
            'stop_button_alt4': 'button[title*="Stop"]',
            'stop_button_alt5': '.stop-button'
        }

    def login(self):
        logger.info("Navigating to Deepseek...")

        selectors = self.get_selectors()
        input_selectors = [
            selectors['input_box'],
            selectors['input_box_alt'],
            selectors['input_box_alt2'],
            selectors['input_box_alt3']
        ]

        for selector in input_selectors:
            try:
                self.wait_for_element(selector, timeout=3)
                logger.info("Already logged in!")
                return True
            except:
                continue

        logger.error("❌ NOT LOGGED IN! Please ensure you are logged into Deepseek before running automation.")
        logger.error("❌ Open Chrome, go to https://chat.deepseek.com, log in, then run automation.")
        return False

    def send_prompt(self, prompt_text, wait_for_completion=True, skip_model_verification=False):
        selectors = self.get_selectors()
        start_time = time.time()

        original_prompt = prompt_text
        prompt_text = prompt_text.replace('\n', ' ').replace('\r', ' ')
        import re
        prompt_text = re.sub(r'\s+', ' ', prompt_text).strip()

        logger.info(f"🔄 Converted prompt: {len(original_prompt)} chars → {len(prompt_text)} chars (removed newlines)")

        try:
            logger.debug("=== DEBUGGING INPUT ELEMENTS ===")
            all_possible_inputs = self.driver.find_elements(By.CSS_SELECTOR, "textarea, input, [contenteditable], [role='textbox']")
            logger.debug(f"Found {len(all_possible_inputs)} potential input elements:")
            for i, elem in enumerate(all_possible_inputs):
                try:
                    tag_name = elem.tag_name
                    classes = elem.get_attribute('class') or 'no-class'
                    placeholder = elem.get_attribute('placeholder') or 'no-placeholder'
                    role = elem.get_attribute('role') or 'no-role'
                    contenteditable = elem.get_attribute('contenteditable') or 'no-contenteditable'
                    is_displayed = elem.is_displayed()
                    logger.debug(f"  {i+1}. {tag_name} - class:'{classes}' placeholder:'{placeholder}' role:'{role}' contenteditable:'{contenteditable}' displayed:{is_displayed}")
                except:
                    logger.debug(f"  {i+1}. Error getting element info")
            logger.debug("=== END INPUT ELEMENTS DEBUG ===")

            input_box = None
            used_input_selector = None
            input_selectors = [
                selectors['input_box'],
                selectors['input_box_alt'],
                selectors['input_box_alt2'],
                selectors['input_box_alt3']
            ]

            for selector in input_selectors:
                try:
                    input_box = self.wait_for_element(selector, timeout=3)
                    used_input_selector = selector
                    logger.debug(f"Found input box: {selector}")
                    break
                except:
                    continue

            if not input_box:
                logger.error("Could not find input box with any selector")

                for elem in all_possible_inputs:
                    try:
                        if elem.is_displayed() and elem.is_enabled():
                            input_box = elem
                            used_input_selector = "fallback-visible-input"
                            logger.debug("Using fallback visible input element")
                            break
                    except:
                        continue

                if not input_box:
                    return None

            input_box.click()
            time.sleep(1)

            working_input = None

            deepseek_input_patterns = [
                'div[data-placeholder]',
                'div[contenteditable="plaintext-only"]',
                'div[contenteditable="true"][role="textbox"]',
                '[data-testid="chat-input"]',
                '[data-testid="message-input"]',
                'div.input-container [contenteditable]',
                'div.chat-input [contenteditable]',

                'textarea[placeholder*="message" i]',
                'textarea[placeholder*="ask" i]',
                'div[contenteditable="true"]',
                'textarea',
                '[role="textbox"]'
            ]

            logger.debug("Searching for REAL Deepseek input element...")
            for pattern in deepseek_input_patterns:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, pattern)
                    for elem in elements:
                        if elem.is_displayed() and elem.is_enabled():
                            try:
                                elem.click()
                                is_editable = (elem.get_attribute('contenteditable') == 'true' or
                                             elem.tag_name.lower() == 'textarea' or
                                             elem.tag_name.lower() == 'input')

                                current_content = elem.get_attribute('value') or elem.get_attribute('textContent') or elem.text

                                if is_editable:
                                    working_input = elem
                                    logger.info(f"Found WORKING input element: {pattern}")
                                    break
                            except:
                                continue
                    if working_input:
                        break
                except:
                    continue

            if not working_input:
                logger.error("Could not find any working input element!")
                return None

            try:
                logger.debug("Using direct input with verified working element")

                working_input.clear()
                time.sleep(0.2)

                working_input.send_keys(prompt_text)
                time.sleep(0.5)

                current_text = working_input.get_attribute('value') or working_input.get_attribute('textContent') or working_input.text
                if len(current_text) < len(prompt_text) * 0.8:
                    raise Exception(f"Text not fully entered: {len(current_text)}/{len(prompt_text)}")

                working_input.send_keys(Keys.RETURN)

                text_set_successfully = True
                logger.info(f"✅ Text sent successfully via direct input: {len(current_text)} chars")

                if wait_for_completion:
                    response = self.wait_for_response()
                    self.last_response_time = time.time() - start_time
                    logger.info(f"🕒 Total response time: {self.last_response_time:.2f}s")
                    return response

                return True

            except Exception as e:
                logger.debug(f"Direct input failed: {e}")
                try:
                    logger.debug("Trying clipboard method with working element")
                    import pyperclip
                    pyperclip.copy(prompt_text)

                    working_input.clear()
                    working_input.send_keys(Keys.CONTROL, 'v')
                    time.sleep(0.5)

                    current_text = working_input.get_attribute('value') or working_input.get_attribute('textContent') or working_input.text
                    if len(current_text) > len(prompt_text) * 0.8:
                        working_input.send_keys(Keys.RETURN)
                        text_set_successfully = True
                        logger.info(f"✅ Text sent via clipboard: {len(current_text)} chars")

                        if wait_for_completion:
                            response = self.wait_for_response()
                            self.last_response_time = time.time() - start_time
                            logger.info(f"🕒 Total response time: {self.last_response_time:.2f}s")
                            return response

                        return True
                    else:
                        raise Exception("Clipboard paste incomplete")

                except Exception as e2:
                    logger.debug(f"Clipboard failed: {e2} (likely pyperclip not installed)")
                    logger.debug("Using JavaScript approach with working element")

                    try:
                        fresh_working_input = None
                        for pattern in deepseek_input_patterns:
                            try:
                                elements = self.driver.find_elements(By.CSS_SELECTOR, pattern)
                                for elem in elements:
                                    if elem.is_displayed() and elem.is_enabled():
                                        fresh_working_input = elem
                                        break
                                if fresh_working_input:
                                    break
                            except:
                                continue

                        if not fresh_working_input:
                            raise Exception("Could not find fresh working input element")

                        self.driver.execute_script("""
                        var element = arguments[0];
                        var text = arguments[1];
                        
                        // Focus first
                        element.focus();
                        element.click();
                        
                        // Check if it's a textarea or contenteditable
                        if (element.tagName.toLowerCase() === 'textarea' || element.type === 'textarea') {
                            // For textarea elements
                            element.value = '';
                            element.value = text;
                        } else {
                            // For contenteditable elements
                            element.innerHTML = '';
                            element.textContent = text;
                        }
                        
                        // Trigger input events
                        element.dispatchEvent(new Event('input', { bubbles: true }));
                        element.dispatchEvent(new Event('change', { bubbles: true }));
                        
                        console.log('Text set in Deepseek via JavaScript:', text.length, 'characters');
                        """, fresh_working_input, prompt_text)

                        time.sleep(1)
                        current_text = fresh_working_input.get_attribute('value') or fresh_working_input.get_attribute('textContent') or fresh_working_input.text
                        if len(current_text) > len(prompt_text) * 0.8:
                            fresh_working_input.send_keys(Keys.RETURN)
                            text_set_successfully = True
                            logger.info(f"✅ Text sent via JavaScript: {len(current_text)} chars")

                            # If wait_for_completion is True, wait for response
                            if wait_for_completion:
                                response = self.wait_for_response()
                                self.last_response_time = time.time() - start_time
                                logger.info(f"🕒 Total response time: {self.last_response_time:.2f}s")
                                return response

                            return True
                        else:
                            raise Exception("JavaScript insertion incomplete")

                    except Exception as e3:
                        logger.error(f"All text insertion methods failed: direct={e}, clipboard={e2}, javascript={e3}")
                        return None

        except Exception as e:
            logger.error(f"Failed to send prompt: {e}")
            self.last_response_time = 0
            return None

    def wait_for_response(self, max_wait_time=120):
        """Wait for Deepseek response - based on OpenAI logic"""
        selectors = self.get_selectors()
        start_time = time.time()

        logger.info("✅ Waiting for Deepseek response - looking for content generation")

        time.sleep(3)

        logger.info("=== DEBUGGING DEEPSEEK UI ELEMENTS ===")

        all_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
        all_divs = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='loading'], div[class*='generating'], div[class*='typing']")
        all_spans = self.driver.find_elements(By.CSS_SELECTOR, "span[class*='loading'], span[class*='generating'], span[class*='typing']")
        all_svg = self.driver.find_elements(By.CSS_SELECTOR, "svg[class*='spin'], svg[class*='loading'], svg[class*='animate']")

        logger.info(f"Found {len(all_buttons)} buttons, {len(all_divs)} loading divs, {len(all_spans)} loading spans, {len(all_svg)} animated SVGs")

        animated_elements = self.driver.find_elements(By.CSS_SELECTOR, "*[class*='animate'], *[class*='spin'], *[class*='pulse'], *[class*='loading']")
        logger.info(f"Found {len(animated_elements)} potentially animated elements")
        for i, elem in enumerate(animated_elements[:5]):
            try:
                tag = elem.tag_name
                classes = elem.get_attribute('class') or ""
                is_visible = elem.is_displayed()
                logger.info(f"  Animated {i+1}: <{tag}> class='{classes}' visible={is_visible}")
            except:
                pass

        current_url = self.driver.current_url
        logger.info(f"Current URL: {current_url}")

        try:
            input_elements = self.driver.find_elements(By.CSS_SELECTOR, "textarea, input, [contenteditable]")
            logger.info(f"Found {len(input_elements)} input elements during generation")
            for i, elem in enumerate(input_elements[:3]):
                try:
                    is_enabled = elem.is_enabled()
                    is_displayed = elem.is_displayed()
                    placeholder = elem.get_attribute('placeholder') or ""
                    disabled = elem.get_attribute('disabled') or ""
                    readonly = elem.get_attribute('readonly') or ""
                    logger.info(f"  Input {i+1}: enabled={is_enabled} displayed={is_displayed} placeholder='{placeholder}' disabled='{disabled}' readonly='{readonly}'")
                except:
                    pass
        except:
            pass

        logger.info("=== END DEEPSEEK UI DEBUG ===")

        last_response_length = 0
        stable_count = 0
        min_response_length = 500

        while time.time() - start_time < max_wait_time:
            try:
                stop_button_visible = False
                stop_selectors = [
                    selectors['stop_button'],
                    selectors['stop_button_alt'],
                    selectors['stop_button_alt2'],
                    selectors['stop_button_alt3'],
                    selectors['stop_button_alt4'],
                    selectors['stop_button_alt5']
                ]

                for stop_selector in stop_selectors:
                    try:
                        stop_buttons = self.driver.find_elements(By.CSS_SELECTOR, stop_selector)
                        logger.info(f"Checking stop selector '{stop_selector}': found {len(stop_buttons)} elements")
                        for btn in stop_buttons:
                            is_visible = btn.is_displayed()
                            logger.info(f"  Stop button visible: {is_visible}")
                            if is_visible:
                                stop_button_visible = True
                                logger.info(f"✓ Stop button visible ({stop_selector}) - still generating...")
                                break
                        if stop_button_visible:
                            break
                    except Exception as e:
                        logger.info(f"Error checking stop selector '{stop_selector}': {e}")
                        continue

                if stop_button_visible:
                    time.sleep(3)
                    continue

                loading_selectors = [selectors['loading_indicator'], selectors['loading_indicator_alt']]
                is_loading = False
                for loading_selector in loading_selectors:
                    try:
                        loading_indicators = self.driver.find_elements(By.CSS_SELECTOR, loading_selector)
                        logger.info(f"Checking loading selector '{loading_selector}': found {len(loading_indicators)} elements")
                        if loading_indicators and any(elem.is_displayed() for elem in loading_indicators):
                            logger.info(f"Loading indicator visible ({loading_selector}) - still generating...")
                            is_loading = True
                            break
                    except Exception as e:
                        logger.info(f"Error checking loading selector '{loading_selector}': {e}")
                        continue

                if is_loading:
                    time.sleep(3)
                    continue

                elapsed_time = time.time() - start_time
                logger.info(f"🔍 No generation indicators visible after {elapsed_time:.1f}s - generation appears finished")

                response_text = None

                response_selectors = [
                    selectors['response_text'],
                    selectors['response_text_alt'],
                    selectors['response_text_alt2'],
                    selectors['response_text_alt3'],
                    '.message-content .markdown',
                    '.message-content div',
                    '[data-role="assistant"]',
                    '.assistant-message',
                    '.response-message',
                    '.chat-message'
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

                if not response_text:
                    logger.debug("No response found via selectors, trying JavaScript...")
                    try:
                        js_response = self.driver.execute_script("""
                            // Search for Deepseek's response - look for test code specifically
                            var keywords = ['import unittest', 'class Test', 'def test_', 'unittest.TestCase', 'import ', 'from ', 'class ', 'def '];
                            var allElements = Array.from(document.querySelectorAll('*'));
                            var bestMatch = '';
                            var bestScore = 0;
                            
                            for (var elem of allElements) {
                                var text = elem.textContent || elem.innerText || '';
                                // Skip our prompt and look for substantial test code
                                if (text.length > 500 && 
                                    !text.includes('Generate a complete Python unit test suite') &&
                                    !text.includes('Ask me anything')) {
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

                    if current_length > min_response_length:
                        self.response_time = time.time() - start_time
                        logger.info(f"Response received in {self.response_time:.2f}s ({len(response_text)} chars)")
                        return response_text
                    else:
                        logger.warning(f"Short response detected after generation finished: {current_length} chars")
                        time.sleep(2)
                        continue
                else:
                    logger.debug("No response text found yet, waiting...")
                    time.sleep(2)
                    continue

            except Exception as e:
                logger.debug(f"Waiting for response: {e}")
                time.sleep(3)

        logger.error("Response timeout")
        return None

    def start_new_chat(self):
        """Start new chat - try multiple selectors"""
        selectors = self.get_selectors()
        new_chat_selectors = [
            selectors['new_chat_button'],
            selectors['new_chat_button_alt'],
            selectors['new_chat_button_alt2']
        ]

        for selector in new_chat_selectors:
            try:
                new_chat_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                new_chat_button.click()
                logger.info(f"New chat started using: {selector}")
                time.sleep(3)
                return True
            except:
                continue

        logger.warning("Could not find new chat button - continuing without starting new chat")
        return True

    def extract_code_from_response(self, response_text):
        import re

        code_blocks = re.findall(r'```python\n(.*?)\n```', response_text, re.DOTALL)
        if code_blocks:
            return code_blocks[0]

        code_blocks = re.findall(r'```\n(.*?)\n```', response_text, re.DOTALL)
        if code_blocks:
            for block in code_blocks:
                if 'import' in block or 'class' in block or 'def' in block:
                    return block

        if ('import' in response_text and 'class' in response_text and
            'def' in response_text and len(response_text) > 100):
            return response_text

        return None

    def select_model(self):
        logger.info("Skipping model selection - user will select manually")
        return True