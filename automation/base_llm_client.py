"""
Bazowa klasa do automatyzacji interakcji z LLM przez przeglądarki internetowe
"""
import time
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseLLMClient(ABC):
    """Bazowa klasa dla wszystkich klientów LLM"""
    
    def __init__(self, headless=True, timeout=30):
        self.timeout = timeout
        self.response_time = 0
        self.driver = None
        self.use_profile = getattr(self, 'use_profile', False)
        self.setup_driver(headless)
    
    def setup_driver(self, headless=True):
        """Konfiguracja przeglądarki Chrome z opcjami anti-detection"""
        chrome_options = Options()
        
        # Opcja 1: Podłącz do istniejącej przeglądarki (PRIORYTET!)
        if getattr(self, 'attach_to_existing', False):
            debug_port = getattr(self, 'debug_port', 9222)
            chrome_options.add_experimental_option("debuggerAddress", f"localhost:{debug_port}")
            print(f"Connecting to existing browser on port {debug_port}")
            # WAŻNE: Wyłącz wszystkie dodatkowe opcje gdy się podłączasz!
            self.use_profile = False
            # Połącz się minimalistycznie
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, self.timeout)
            return
        
        # Opcja 2: Użyj domyślnego profilu Chrome użytkownika  
        elif self.use_profile:
            from profile_finder import find_chrome_profile
            import random
            chrome_dir = find_chrome_profile()
            if chrome_dir:
                chrome_options.add_argument(f"--user-data-dir={chrome_dir}")
                chrome_options.add_argument("--profile-directory=Default")
                # Unikalny port dla remote debugging
                debug_port = random.randint(9222, 9999)
                chrome_options.add_argument(f"--remote-debugging-port={debug_port}")
                print(f"Using Chrome profile: {chrome_dir}/Default (port: {debug_port})")
            else:
                print("Chrome profile not found, using default settings")
        
        # Podstawowe opcje
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Anti-detection opcje (tylko jeśli nie używamy profilu)
        if not self.use_profile:
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Opcje dla lepszej wydajności
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Ukryj właściwości webdriver (tylko jeśli nie używamy profilu)
        if not self.use_profile:
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.wait = WebDriverWait(self.driver, self.timeout)
    
    @abstractmethod
    def login(self):
        """Logowanie do platformy (jeśli wymagane)"""
        pass
    
    @abstractmethod
    def send_prompt(self, prompt_text):
        """Wysłanie promptu i otrzymanie odpowiedzi"""
        pass
    
    @abstractmethod
    def get_selectors(self):
        """Zwraca słownik z selektorami CSS dla danej platformy"""
        pass
    
    def measure_response_time(self, func, *args, **kwargs):
        """Pomiar czasu odpowiedzi"""
        start_time = time.time()
        result = func(*args, **kwargs)
        self.response_time = time.time() - start_time
        logger.info(f"Response time: {self.response_time:.2f} seconds")
        return result
    
    def wait_for_element(self, selector, timeout=None):
        """Czeka na pojawienie się elementu"""
        if timeout is None:
            timeout = self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element
        except TimeoutException:
            logger.error(f"Element not found: {selector}")
            raise
    
    def wait_for_clickable(self, selector, timeout=None):
        """Czeka aż element będzie klikalny"""
        if timeout is None:
            timeout = self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            return element
        except TimeoutException:
            logger.error(f"Element not clickable: {selector}")
            raise
    
    def safe_click(self, selector):
        """Bezpieczne kliknięcie z retry"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                element = self.wait_for_clickable(selector)
                element.click()
                return True
            except Exception as e:
                logger.warning(f"Click attempt {attempt + 1} failed: {e}")
                time.sleep(1)
        return False
    
    def safe_send_keys(self, selector, text, clear_first=True):
        """Bezpieczne wysłanie tekstu"""
        try:
            element = self.wait_for_element(selector)
            if clear_first:
                element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            logger.error(f"Failed to send keys: {e}")
            return False
    
    def extract_response_text(self, selector):
        """Wyciągnięcie tekstu odpowiedzi"""
        try:
            element = self.wait_for_element(selector)
            return element.text
        except Exception as e:
            logger.error(f"Failed to extract response: {e}")
            return None
    
    def cleanup(self):
        """Zamknięcie przeglądarki"""
        if self.driver:
            self.driver.quit()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()