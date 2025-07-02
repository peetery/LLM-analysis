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
import os
import platform

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
        """Konfiguracja przeglądarki Chrome z opcjami anti-detection i obsługą WSL"""
        chrome_options = Options()
        
        # Sprawdź WSL
        is_wsl = self.is_wsl()
        if is_wsl:
            logger.info("🐧 WSL detected - configuring for Windows Chrome")
            
        # Opcja 1: Podłącz do istniejącej przeglądarki (PRIORYTET!)
        if getattr(self, 'attach_to_existing', False):
            debug_port = getattr(self, 'debug_port', 9222)
            
            # W WSL użyj IP Windows hosta zamiast localhost
            if is_wsl:
                # Pobierz IP Windows hosta z WSL
                debug_host = self.get_windows_host_ip()
                print(f"🐧 WSL: Connecting to Windows Chrome at {debug_host}:{debug_port}")
            else:
                debug_host = "localhost"
                print(f"Connecting to existing browser on port {debug_port}")
            
            chrome_options.add_experimental_option("debuggerAddress", f"{debug_host}:{debug_port}")
            # WAŻNE: Wyłącz wszystkie dodatkowe opcje gdy się podłączasz!
            self.use_profile = False
            
            # WSL: Ustaw ścieżkę do Chrome
            chrome_executable = self.get_chrome_executable_path()
            
            # Połącz się minimalistycznie
            if chrome_executable and is_wsl:
                # W WSL używaj Chrome z Windows ale bez executable_path (deprecated)
                self.driver = webdriver.Chrome(options=chrome_options)
                logger.warning("WSL: Using Windows Chrome via remote debugging")
            else:
                self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, self.timeout)
            return
        
        # Opcja 2: Użyj domyślnego profilu Chrome użytkownika  
        elif self.use_profile:
            from profile_finder import find_chrome_profile
            import random
            chrome_dir = find_chrome_profile()
            if chrome_dir:
                # W WSL użyj bezpieczniejszej ścieżki
                if is_wsl:
                    # Skopiuj profil do WSL temp
                    wsl_profile_dir = f"/tmp/chrome_profile_{random.randint(1000, 9999)}"
                    os.makedirs(wsl_profile_dir, exist_ok=True)
                    chrome_options.add_argument(f"--user-data-dir={wsl_profile_dir}")
                else:
                    chrome_options.add_argument(f"--user-data-dir={chrome_dir}")

                chrome_options.add_argument("--profile-directory=Default")
                # Unikalny port dla remote debugging
                debug_port = random.randint(9222, 9999)
                chrome_options.add_argument(f"--remote-debugging-port={debug_port}")
                print(f"Using Chrome profile (port: {debug_port})")
            else:
                print("Chrome profile not found, using default settings")

        # Podstawowe opcje
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        # WSL-specific opcje
        if is_wsl:
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-features=TranslateUI")
            chrome_options.add_argument("--disable-ipc-flooding-protection")

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

        # WSL: Nie ustawiaj executable_path, selenium znajdzie Chrome automatycznie
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

    def is_wsl(self):
        """Wykrywa czy skrypt działa w WSL"""
        try:
            with open('/proc/version', 'r') as f:
                version_info = f.read().lower()
                return 'microsoft' in version_info or 'wsl' in version_info
        except:
            return False

    def get_chrome_executable_path(self):
        """Znajduje ścieżkę do Chrome (obsługuje WSL)"""
        if self.is_wsl():
            # W WSL, szukaj Chrome z Windows
            windows_chrome_paths = [
                '/mnt/c/Program Files/Google/Chrome/Application/chrome.exe',
                '/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe'
            ]

            for path in windows_chrome_paths:
                if os.path.exists(path):
                    logger.info(f"✓ Found Windows Chrome in WSL: {path}")
                    return path

            logger.warning("⚠️  Chrome not found in standard Windows locations from WSL")
            return None
        else:
            # Linux/Windows native - selenium znajdzie automatycznie
            return None

    def get_windows_host_ip(self):
        """Pobiera IP Windows hosta z WSL"""
        try:
            import subprocess
            # Pobierz IP z /etc/resolv.conf (default gateway w WSL2)
            result = subprocess.run(['cat', '/etc/resolv.conf'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if line.startswith('nameserver'):
                    ip = line.split()[1]
                    logger.info(f"✓ Windows host IP: {ip}")
                    return ip
            
            # Fallback - spróbuj hostname
            result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
            if result.stdout.strip():
                # Weź pierwszy IP z listy
                ip = result.stdout.strip().split()[0]
                # Zamień ostatni oktet na 1 (typowy gateway)
                ip_parts = ip.split('.')
                if len(ip_parts) == 4:
                    gateway_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.1"
                    logger.info(f"✓ Fallback Windows host IP: {gateway_ip}")
                    return gateway_ip
            
            # Hard fallback
            logger.warning("⚠️  Could not detect Windows host IP, using default")
            return "172.16.0.1"  # Domyślny gateway w WSL2
            
        except Exception as e:
            logger.error(f"Error getting Windows host IP: {e}")
            return "172.16.0.1"
