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
        """Logowanie do ChatGPT z weryfikacją modelu"""
        logger.info("Navigating to ChatGPT...")
        
        # Sprawdź czy już zalogowany
        try:
            self.wait_for_element(self.get_selectors()['input_box'], timeout=5)
            logger.info("Already logged in!")
            
            # Weryfikuj czy właściwy model jest wybrany
            if self.verify_and_ensure_model():
                return True
            else:
                logger.warning("Model verification failed, but continuing...")
                return True
                
        except:
            logger.error("❌ NOT LOGGED IN! Please ensure you are logged into ChatGPT before running automation.")
            logger.error("❌ Open Chrome, go to https://chatgpt.com, log in, then run automation.")
            return False
    
    def send_prompt(self, prompt_text, wait_for_completion=True):
        """Send prompt to ChatGPT with model verification"""
        selectors = self.get_selectors()
        start_time = time.time()  # Start timing from here
        
        # KLUCZOWE: Sprawdź model przed wysłaniem promptu
        logger.info(f"🔍 Verifying model before sending prompt...")
        if not self.verify_and_ensure_model():
            logger.warning("⚠️  Model verification failed, but continuing with prompt")
        
        # Sprawdź czy nie ma alertów/popupów
        self.handle_popups_and_alerts()
        
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
                # Try to send with retry if button stays enabled
                max_attempts = 3
                sent_successfully = False
                
                for attempt in range(max_attempts):
                    send_button.click()
                    logger.info(f"Prompt send attempt {attempt + 1}/{max_attempts}")
                    
                    # Wait and verify that message was sent
                    time.sleep(2)
                    try:
                        # Re-find send button to check its state
                        new_send_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button[data-testid="send-button"]')
                        if new_send_buttons:
                            new_send_button = new_send_buttons[0]
                            is_disabled = new_send_button.get_attribute('disabled') or not new_send_button.is_enabled()
                            if is_disabled:
                                logger.info("✅ Message sending verified - send button disabled")
                                sent_successfully = True
                                break
                            else:
                                logger.warning(f"⚠️  Attempt {attempt + 1}: Send button still enabled - message not sent!")
                                if attempt < max_attempts - 1:
                                    logger.info("🔄 Retrying send...")
                                    # Update send_button reference for next attempt
                                    send_button = new_send_button
                        else:
                            logger.info("✅ Send button disappeared - likely sent successfully")
                            sent_successfully = True
                            break
                    except Exception as e:
                        logger.info(f"✅ Send button verification failed (likely due to page change) - assuming sent: {e}")
                        sent_successfully = True
                        break
                
                if not sent_successfully:
                    logger.error("❌ Failed to send message after 3 attempts - send button never disabled")
                    self.last_response_time = 0
                    return None
                
                if wait_for_completion:
                    try:
                        response = self.wait_for_response()
                        # Calculate and store response time
                        self.last_response_time = time.time() - start_time
                        logger.info(f"🕒 Total response time: {self.last_response_time:.2f}s")
                        return response
                    except Exception as e:
                        logger.error(f"Failed while waiting for response: {e}")
                        self.last_response_time = time.time() - start_time
                        logger.warning(f"⚠️  Prompt sent but response waiting failed after {self.last_response_time:.2f}s")
                        return None
                return True
            else:
                logger.error("Send button not found")
                self.last_response_time = 0
                return None
            
        except Exception as e:
            logger.error(f"Failed to send prompt: {e}")
            return None
    
    def wait_for_response(self, max_wait_time=180):
        """Wait for ChatGPT response"""
        selectors = self.get_selectors()
        start_time = time.time()
        
        logger.info("Waiting for ChatGPT response...")
        
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
        
        # Wait for generation to continue
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
                
                # Also check for Canvas generation indicators
                canvas_loading = self.driver.find_elements(By.CSS_SELECTOR, '.canvas-loading, .canvas .loading, .canvas .generating')
                if canvas_loading and any(elem.is_displayed() for elem in canvas_loading):
                    logger.debug("Canvas is still generating...")
                    time.sleep(3)
                    continue
                
                # Secondary check: send button state
                send_buttons = self.driver.find_elements(By.CSS_SELECTOR, selectors['send_button'])
                if send_buttons:
                    send_button = send_buttons[0]
                    is_disabled = send_button.get_attribute('disabled') or not send_button.is_enabled()
                    
                    if not is_disabled:
                        # Send button is ENABLED - this means NO generation is happening
                        logger.warning("Send button is enabled - no generation happening, probably message not sent!")
                        return None  # Return None to indicate failure
                    else:
                        logger.debug("Send button disabled - still generating...")
                        time.sleep(3)
                        continue
                
                # Get response from BOTH normal chat AND Canvas
                response_text = None
                
                # Try Canvas first (if present, it usually contains the main response)
                logger.debug("Searching for Canvas response...")
                canvas_selectors = [
                    # Direct Canvas content
                    '.canvas-content', '[data-testid="canvas-content"]', 
                    '.canvas-editor', '.canvas .code-block',
                    '.canvas pre', '.canvas code',
                    
                    # Alternative Canvas patterns
                    '[class*="canvas"] pre', '[class*="canvas"] code',
                    '[class*="Canvas"] pre', '[class*="Canvas"] code',
                    
                    # IFrame content (if Canvas is in iframe)
                    'iframe', 
                    
                    # Monaco Editor (common code editor)
                    '.monaco-editor', '.monaco-editor .view-lines',
                    
                    # General code editors
                    '.code-editor', '.editor-content',
                    '[role="textbox"][contenteditable]',
                    
                    # Text areas that might contain code
                    'textarea', '[contenteditable="true"]'
                ]
                
                for selector in canvas_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            for element in elements:
                                text = element.text.strip()
                                # IMPORTANT: Skip our own prompt! Look for test code specifically
                                if (text and len(text) > 1000 and  # Zmniejszona minimalna długość
                                    ('import unittest' in text or 'class Test' in text or 'def test_' in text) and
                                    'Generate a complete Python unit test suite' not in text):  # Skip our prompt
                                    response_text = text
                                    logger.info(f"✓ Found response in Canvas: {len(text)} chars")
                                    break
                            if response_text:
                                break
                    except:
                        continue
                
                # If not found in Canvas, try normal chat selectors
                if not response_text:
                    logger.debug("Canvas not found, searching normal chat...")
                    chat_selectors = [
                        '[data-message-author-role="assistant"]',
                        '[data-testid="conversation-turn"]:last-child [data-message-author-role="assistant"]',
                        '.markdown',
                        '[role="article"]',
                        '.message-content'
                    ]
                    
                    for selector in chat_selectors:
                        try:
                            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            if elements:
                                last_element = elements[-1]
                                text = last_element.text.strip()
                                # Skip our prompt and look for actual response
                                if (text and len(text) > len(response_text or "") and 
                                    'Generate a complete Python unit test suite' not in text and
                                    len(text) > 500):  # Response should be substantial
                                    response_text = text
                                    logger.info(f"✓ Found response in chat: {len(text)} chars")
                        except:
                            continue
                
                # Fallback: Use JavaScript to find any text that looks like code (only if nothing found)
                if not response_text:
                    logger.debug("No response found via selectors, trying JavaScript...")
                    try:
                        js_response = self.driver.execute_script("""
                            // More aggressive search for Python code
                            var keywords = ['import unittest', 'class Test', 'def test_', 'unittest.TestCase', 'import ', 'from ', 'class ', 'def '];
                            var allElements = Array.from(document.querySelectorAll('*'));
                            var bestMatch = '';
                            var bestScore = 0;
                            
                            for (var elem of allElements) {
                                var text = elem.textContent || elem.innerText || elem.value || '';
                                // Skip our prompt and look for substantial test code
                                if (text.length > 2000 && 
                                    !text.includes('Generate a complete Python unit test suite')) {
                                    var score = 0;
                                    for (var keyword of keywords) {
                                        if (text.includes(keyword)) {
                                            score += keyword.length;
                                        }
                                    }
                                    if (score > bestScore) {
                                        bestScore = score;
                                        bestMatch = text;
                                    }
                                }
                            }
                            
                            return bestMatch || null;
                        """)
                        
                        if js_response and len(js_response) > len(response_text or ""):
                            response_text = js_response
                            logger.info(f"✓ Found response via JavaScript: {len(js_response)} chars")
                    except Exception as e:
                        logger.debug(f"JavaScript fallback failed: {e}")
                
                if response_text:
                    current_length = len(response_text)
                    
                    # For responses > 100k chars, we probably found the whole page content
                    # This is likely the Canvas content we want!
                    if current_length > 100000:
                        logger.info(f"Large response detected ({current_length} chars) - likely Canvas content")
                        self.response_time = time.time() - start_time
                        return response_text
                    
                    # For Canvas responses (substantial code), return immediately
                    if current_length > 3000 and ('import unittest' in response_text or 'class Test' in response_text):
                        logger.info(f"Canvas code response detected ({current_length} chars)")
                        self.response_time = time.time() - start_time
                        return response_text
                    
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
        """Start new chat with model verification"""
        logger.info("🆕 Starting new chat...")
        
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
                            
                            # Po rozpoczęciu nowego chatu, sprawdź model
                            time.sleep(2)  # Daj czas na załadowanie
                            if not self.verify_and_ensure_model():
                                logger.warning("⚠️  Model verification failed after new chat")
                            
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
                
                # Po nawigacji, sprawdź model
                if not self.verify_and_ensure_model():
                    logger.warning("⚠️  Model verification failed after navigation")
                
                return True
        except:
            pass
            
        logger.warning("Could not start new chat")
        return False
    
    def select_model(self, model_name):
        """Select specific GPT model if available"""
        try:
            logger.info(f"Attempting to select model: {model_name}")
            
            # For GPT-4.5, we need to look for "More models" or similar
            if "4.5" in model_name:
                # First try to find "More models" button or similar
                more_buttons = [
                    'button:contains("More")',
                    'button[aria-label*="More"]',
                    'button:has-text("More")',
                    '[data-testid="more-models"]'
                ]
                
                for selector in more_buttons:
                    try:
                        # Use JavaScript to find buttons with "More" text
                        elements = self.driver.execute_script("""
                            return Array.from(document.querySelectorAll('button')).filter(
                                btn => btn.textContent.toLowerCase().includes('more')
                            );
                        """)
                        
                        if elements:
                            elements[0].click()
                            time.sleep(3)
                            logger.info("Clicked 'More models' button")
                            break
                    except:
                        continue
            
            # Try to find and click model selector
            model_selectors = [
                '[data-testid="model-switcher"]',
                'button[aria-haspopup="menu"]',
                '.model-selector',
                'button:has(svg)',
                '[role="button"]:has-text("GPT")'
            ]
            
            for selector in model_selectors:
                try:
                    # Try CSS selector first
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if not elements:
                        # Try finding buttons with GPT text using JavaScript
                        elements = self.driver.execute_script("""
                            return Array.from(document.querySelectorAll('button, [role="button"]')).filter(
                                btn => btn.textContent.toLowerCase().includes('gpt') || 
                                       btn.getAttribute('aria-label')?.toLowerCase().includes('model')
                            );
                        """)
                    
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            element.click()
                            time.sleep(3)
                            logger.info("Clicked model selector")
                            
                            # Look for specific model option with JavaScript
                            model_found = self.driver.execute_script("""
                                var modelName = arguments[0];
                                var options = Array.from(document.querySelectorAll('[role="menuitem"], [role="option"], button, a'));
                                
                                for (var option of options) {
                                    var text = option.textContent.toLowerCase();
                                    if (text.includes('4.5') || text.includes('gpt-4.5')) {
                                        option.click();
                                        return true;
                                    }
                                }
                                return false;
                            """, model_name)
                            
                            if model_found:
                                time.sleep(2)
                                logger.info(f"✓ Selected model: {model_name}")
                                return True
                            break
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            logger.warning(f"Could not select specific model {model_name}, using default")
            return True  # Continue anyway
            
        except Exception as e:
            logger.warning(f"Model selection failed: {e}")
            return True  # Continue anyway
    
    def verify_and_ensure_model(self):
        """Weryfikuje czy właściwy model jest wybrany i wymusza go AUTOMATYCZNIE"""
        try:
            # Sprawdź aktualnie wybrany model
            current_model = self.get_current_model()
            target_model = self.get_target_model_name()
            
            logger.info(f"🔍 Current model: {current_model}, Target: {target_model}")
            
            if self.is_correct_model(current_model, target_model):
                logger.info(f"✅ Correct model already selected: {current_model}")
                return True
            else:
                logger.warning(f"🔄 AUTO-SWITCHING: Current: {current_model} → Target: {target_model}")
                
                # AUTOMATYCZNIE wymuś właściwy model
                success = self.force_model_selection()
                if success:
                    # Sprawdź ponownie
                    new_model = self.get_current_model()
                    if self.is_correct_model(new_model, target_model):
                        logger.info(f"✅ AUTO-SWITCH SUCCESS: {new_model}")
                        return True
                    else:
                        logger.error(f"❌ AUTO-SWITCH FAILED: Still {new_model}, expected {target_model}")
                        return False
                else:
                    logger.error(f"❌ AUTO-SWITCH FAILED: Could not change model")
                    return False
                
        except Exception as e:
            logger.warning(f"Model verification error: {e}")
            return False
    
    def get_current_model(self):
        """Wykrywa aktualnie wybrany model ChatGPT"""
        try:
            # Szukaj różnych selektorów dla nazwy modelu
            model_selectors = [
                '[data-testid="model-switcher"] span',
                'button[aria-haspopup="menu"] span',
                '.model-name',
                'button:contains("GPT")',
                '[role="button"] span'
            ]
            
            for selector in model_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text.strip().lower()
                        if any(model in text for model in ['gpt', 'o1', 'o3', '4o', '4.5']):
                            return text
                except:
                    continue
            
            # Fallback - użyj JavaScript do znalezienia tekstu modelu
            model_text = self.driver.execute_script("""
                // Szukaj wszystkich elementów z tekstem zawierającym nazwy modeli
                var allElements = Array.from(document.querySelectorAll('*'));
                var modelKeywords = ['gpt-4.5', 'gpt-4o', 'gpt-o3', 'gpt o3', 'o3', '4.5', '4o-mini'];
                
                for (var elem of allElements) {
                    var text = elem.textContent || elem.innerText || '';
                    var lowerText = text.toLowerCase().trim();
                    
                    // Sprawdź czy element jest widoczny i ma rozsądną długość
                    if (elem.offsetParent && text.length < 50) {
                        for (var keyword of modelKeywords) {
                            if (lowerText.includes(keyword) && 
                                !lowerText.includes('select') && 
                                !lowerText.includes('choose')) {
                                return lowerText;
                            }
                        }
                    }
                }
                
                // Sprawdź URL - może zawierać informację o modelu
                var url = window.location.href;
                if (url.includes('model=')) {
                    var match = url.match(/model=([^&]+)/);
                    if (match) return match[1];
                }
                
                return null;
            """)
            
            if model_text:
                return model_text.lower().strip()
                
            return "unknown"
            
        except Exception as e:
            logger.debug(f"Error getting current model: {e}")
            return "unknown"
    
    def get_target_model_name(self):
        """Zwraca oczekiwaną nazwę modelu na podstawie self.model_name"""
        model_mapping = {
            'gpt-4.5': ['4.5', 'gpt-4.5', 'gpt 4.5'],
            'gpt-o3': ['o3', 'gpt-o3', 'gpt o3'],
            'gpt-o4-mini-high': ['4o-mini', 'gpt-4o-mini', '4o mini']
        }
        
        return model_mapping.get(self.model_name, [self.model_name])
    
    def is_correct_model(self, current_model, target_variants):
        """Sprawdza czy aktualny model pasuje do oczekiwanego"""
        if not current_model or current_model == "unknown":
            return False
            
        current_lower = current_model.lower()
        
        # Sprawdź czy któryś z wariantów target jest w current_model
        for variant in target_variants:
            if variant.lower() in current_lower:
                return True
                
        return False
    
    def force_model_selection(self):
        """Wymusza wybór właściwego modelu - PEŁEN AUTOMAT"""
        try:
            logger.info(f"🔄 AUTO-FORCING model selection to: {self.model_name}")
            
            # METODA 1: Refresh strony z odpowiednim URL (2 próby z różnymi wariantami)
            model_urls = [
                {
                    'gpt-4.5': 'https://chatgpt.com/?model=gpt-4.5',
                    'gpt-o3': 'https://chatgpt.com/?model=o3', 
                    'gpt-o4-mini-high': 'https://chatgpt.com/?model=o4-mini-high'
                },
                {
                    'gpt-4.5': 'https://chatgpt.com/?model=gpt4.5',
                    'gpt-o3': 'https://chatgpt.com/?model=gpt-o3',
                    'gpt-o4-mini-high': 'https://chatgpt.com/?model=4o-mini'
                },
                {
                    'gpt-4.5': 'https://chatgpt.com/?model=4.5',
                    'gpt-o3': 'https://chatgpt.com/?model=o3-preview',
                    'gpt-o4-mini-high': 'https://chatgpt.com/?model=mini'
                }
            ]
            
            for i, urls in enumerate(model_urls):
                target_url = urls.get(self.model_name)
                if target_url:
                    logger.info(f"🔗 AUTO-TRY #{i+1}: {target_url}")
                    self.driver.get(target_url)
                    time.sleep(7)  # Dłużej czekaj
                    
                    # Obsłuż popupy które mogą się pojawić
                    self.handle_popups_and_alerts()
                    
                    # Sprawdź czy się udało
                    new_model = self.get_current_model()
                    logger.info(f"🔍 After URL #{i+1}: detected model = {new_model}")
                    
                    if self.is_correct_model(new_model, self.get_target_model_name()):
                        logger.info(f"✅ AUTO-SUCCESS via URL #{i+1}: {new_model}")
                        return True
            
            # METODA 2: Próby automatycznego klikania w interface
            logger.info("🖱️ AUTO-TRYING interface selection...")
            if self.select_model_via_interface():
                return True
            
            # METODA 3: Force poprzez JavaScript
            logger.info("🔧 AUTO-TRYING JavaScript selection...")
            if self.select_model_with_javascript():
                return True
                
            # OSTATNIA PRÓBA: Nawiguj do głównej i spróbuj ponownie
            logger.warning("🔄 LAST AUTO-ATTEMPT: Navigate to home and retry...")
            self.driver.get("https://chatgpt.com/")
            time.sleep(5)
            self.handle_popups_and_alerts()
            
            # Sprawdź model po nawigacji do home
            final_model = self.get_current_model()
            if self.is_correct_model(final_model, self.get_target_model_name()):
                logger.info(f"✅ AUTO-SUCCESS via home navigation: {final_model}")
                return True
            
            logger.error(f"❌ ALL AUTO-METHODS FAILED. Final model: {final_model}")
            return False
            
        except Exception as e:
            logger.error(f"Auto force model selection failed: {e}")
            return False
    
    def select_model_via_interface(self):
        """Automatyczny wybór modelu przez interfejs"""
        try:
            # Szukaj przycisku zmiany modelu
            model_switcher_selectors = [
                '[data-testid="model-switcher"]',
                'button[aria-haspopup="menu"]',
                'button:has(span:contains("GPT"))',
                '.model-selector',
                '[role="button"]:contains("GPT")'
            ]
            
            for selector in model_switcher_selectors:
                try:
                    # Znajdź i kliknij przełącznik modelu
                    switcher = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if switcher.is_displayed() and switcher.is_enabled():
                        switcher.click()
                        time.sleep(3)
                        logger.info(f"🖱️ Clicked model switcher: {selector}")
                        
                        # Teraz szukaj konkretnego modelu w menu
                        if self.select_model_from_dropdown():
                            return True
                            
                except Exception as e:
                    logger.debug(f"Switcher selector failed: {selector} - {e}")
                    continue
            
            # Fallback - użyj JavaScript
            logger.info("🔍 Trying JavaScript model selection...")
            return self.select_model_with_javascript()
            
        except Exception as e:
            logger.error(f"Manual model selection failed: {e}")
            return False
    
    def select_model_from_dropdown(self):
        """Wybiera model z rozwiniętego menu"""
        try:
            target_variants = self.get_target_model_name()
            
            # Szukaj opcji w menu
            option_selectors = [
                '[role="menuitem"]',
                '[role="option"]', 
                'button',
                'a',
                '.menu-item',
                'li'
            ]
            
            for selector in option_selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    try:
                        text = element.text.strip().lower()
                        if text and any(variant.lower() in text for variant in target_variants):
                            if element.is_displayed() and element.is_enabled():
                                element.click()
                                time.sleep(2)
                                logger.info(f"✅ Selected model from dropdown: {text}")
                                return True
                    except:
                        continue
                        
            return False
            
        except Exception as e:
            logger.debug(f"Dropdown selection failed: {e}")
            return False
    
    def select_model_with_javascript(self):
        """Ostatnia szansa - wybór modelu przez JavaScript"""
        try:
            target_variants = self.get_target_model_name()
            
            success = self.driver.execute_script("""
                var targetVariants = arguments[0];
                var allElements = Array.from(document.querySelectorAll('button, [role="menuitem"], [role="option"], a'));
                
                for (var element of allElements) {
                    var text = (element.textContent || element.innerText || '').toLowerCase().trim();
                    
                    for (var variant of targetVariants) {
                        if (text.includes(variant.toLowerCase()) && 
                            element.offsetParent && // element is visible
                            !element.disabled) {
                            
                            try {
                                element.click();
                                return true;
                            } catch (e) {
                                // Try different click methods
                                try {
                                    element.dispatchEvent(new MouseEvent('click', {bubbles: true}));
                                    return true;
                                } catch (e2) {
                                    continue;
                                }
                            }
                        }
                    }
                }
                return false;
            """, target_variants)
            
            if success:
                time.sleep(3)
                logger.info("✅ Model selected via JavaScript")
                return True
            else:
                logger.warning("❌ JavaScript model selection failed")
                return False
                
        except Exception as e:
            logger.error(f"JavaScript model selection error: {e}")
            return False
    
    def handle_popups_and_alerts(self):
        """Obsługuje popupy i alerty które mogą się pojawiać w ChatGPT"""
        try:
            # Sprawdź JavaScript alerty
            try:
                alert = self.driver.switch_to.alert
                logger.warning(f"🚨 JavaScript alert detected: {alert.text}")
                alert.accept()
                time.sleep(1)
            except:
                pass  # Brak alertu
            
            # Sprawdź modalne okna dialogowe
            modal_selectors = [
                '[role="dialog"]',
                '.modal',
                '.popup',
                '[data-testid="modal"]',
                '.overlay'
            ]
            
            for selector in modal_selectors:
                try:
                    modals = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for modal in modals:
                        if modal.is_displayed():
                            logger.warning(f"🔲 Modal detected: {selector}")
                            
                            # Spróbuj znaleźć przycisk zamknięcia
                            close_selectors = [
                                'button:contains("Close")',
                                'button:contains("OK")', 
                                'button:contains("Accept")',
                                'button:contains("Continue")',
                                '[aria-label="Close"]',
                                '.close-button',
                                'button[data-testid="close"]'
                            ]
                            
                            for close_selector in close_selectors:
                                try:
                                    close_btn = modal.find_element(By.CSS_SELECTOR, close_selector)
                                    if close_btn.is_displayed() and close_btn.is_enabled():
                                        close_btn.click()
                                        logger.info(f"✓ Closed modal with: {close_selector}")
                                        time.sleep(1)
                                        return
                                except:
                                    continue
                            
                            # Jeśli nie znaleziono przycisku, spróbuj kliknąć poza modal
                            try:
                                self.driver.execute_script("arguments[0].click();", modal)
                                time.sleep(1)
                            except:
                                pass
                                
                except:
                    continue
                    
            # Sprawdź notyfikacje o zmianie modelu
            notification_selectors = [
                '.notification',
                '[role="status"]',
                '.toast',
                '.banner',
                '[data-testid="notification"]'
            ]
            
            for selector in notification_selectors:
                try:
                    notifications = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for notification in notifications:
                        if notification.is_displayed():
                            text = notification.text.lower()
                            if any(keyword in text for keyword in ['model', 'switched', 'changed', 'unavailable']):
                                logger.warning(f"📢 Model change notification: {text[:100]}...")
                                
                                # Spróbuj zamknąć notyfikację
                                try:
                                    close_btn = notification.find_element(By.CSS_SELECTOR, 'button, [role="button"]')
                                    close_btn.click()
                                    time.sleep(1)
                                except:
                                    pass
                except:
                    continue
                    
        except Exception as e:
            logger.debug(f"Error handling popups: {e}")
    
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