#!/usr/bin/env python3
"""
Debug script to analyze current Claude.ai structure
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def debug_claude_structure():
    """Analyze current Claude.ai page structure"""
    
    # Setup Chrome
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        print("=== CLAUDE.AI STRUCTURE ANALYSIS ===")
        print(f"Current URL: {driver.current_url}")
        
        # Navigate to Claude if not already there
        if "claude.ai" not in driver.current_url:
            driver.get("https://claude.ai/new")
            time.sleep(3)
        
        print("\n1. SEARCHING FOR INPUT ELEMENTS:")
        input_selectors = [
            'div[contenteditable="true"]',
            '[role="textbox"]',
            'textarea',
            '[data-testid*="input"]',
            '[aria-label*="message"]',
            '[placeholder*="message"]'
        ]
        
        for selector in input_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                elem = elements[0]
                print(f"✓ FOUND INPUT: {selector}")
                print(f"  - Tag: {elem.tag_name}")
                print(f"  - Visible: {elem.is_displayed()}")
                print(f"  - Enabled: {elem.is_enabled()}")
                print(f"  - Classes: {elem.get_attribute('class')}")
                print(f"  - ID: {elem.get_attribute('id')}")
                print(f"  - Aria-label: {elem.get_attribute('aria-label')}")
        
        print("\n2. SEARCHING FOR SEND BUTTONS:")
        send_selectors = [
            'button[aria-label*="Send"]',
            'button[type="submit"]',
            'button:has(svg)',
            '[data-testid*="send"]',
            'button[aria-label*="send"]',
            'button:contains("Send")'
        ]
        
        for selector in send_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    elem = elements[0]
                    print(f"✓ FOUND SEND BUTTON: {selector}")
                    print(f"  - Tag: {elem.tag_name}")
                    print(f"  - Visible: {elem.is_displayed()}")
                    print(f"  - Enabled: {elem.is_enabled()}")
                    print(f"  - Classes: {elem.get_attribute('class')}")
                    print(f"  - Text: {elem.text}")
                    print(f"  - Aria-label: {elem.get_attribute('aria-label')}")
            except:
                pass
        
        print("\n3. SEARCHING FOR MODEL SELECTOR:")
        model_selectors = [
            'button:contains("Claude")',
            'button:contains("Sonnet")',
            '[data-testid*="model"]',
            'button[aria-label*="model"]',
            '.model-selector',
            'button:contains("4")',
            'button:contains("3.7")'
        ]
        
        for selector in model_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    elem = elements[0]
                    print(f"✓ FOUND MODEL ELEMENT: {selector}")
                    print(f"  - Tag: {elem.tag_name}")
                    print(f"  - Text: {elem.text}")
                    print(f"  - Classes: {elem.get_attribute('class')}")
                    print(f"  - Aria-label: {elem.get_attribute('aria-label')}")
            except:
                pass
        
        print("\n4. JAVASCRIPT ANALYSIS:")
        js_result = driver.execute_script("""
            // Find all buttons and their text content
            var buttons = Array.from(document.querySelectorAll('button'));
            var buttonInfo = buttons.map(btn => ({
                text: btn.textContent.trim(),
                classes: btn.className,
                ariaLabel: btn.getAttribute('aria-label'),
                visible: btn.offsetParent !== null
            })).filter(info => info.text.length > 0 || info.ariaLabel);
            
            // Find all contenteditable elements
            var editables = Array.from(document.querySelectorAll('[contenteditable="true"]'));
            var editableInfo = editables.map(el => ({
                tag: el.tagName,
                classes: el.className,
                placeholder: el.getAttribute('placeholder'),
                ariaLabel: el.getAttribute('aria-label'),
                visible: el.offsetParent !== null
            }));
            
            // Find elements containing "Claude", "Sonnet", "model"
            var modelElements = Array.from(document.querySelectorAll('*')).filter(el => {
                var text = el.textContent || '';
                return (text.includes('Claude') || text.includes('Sonnet') || text.includes('model')) && 
                       el.children.length === 0 && text.length < 100;
            }).map(el => ({
                tag: el.tagName,
                text: el.textContent.trim(),
                classes: el.className,
                clickable: el.tagName === 'BUTTON' || el.onclick || el.getAttribute('role') === 'button'
            }));
            
            return {
                buttons: buttonInfo.slice(0, 10),
                editables: editableInfo,
                modelElements: modelElements.slice(0, 10)
            };
        """)
        
        print("BUTTONS found via JS:")
        for btn in js_result['buttons']:
            print(f"  - Text: '{btn['text']}' | Classes: {btn['classes']} | Aria: {btn['ariaLabel']}")
        
        print("\nEDITABLE elements:")
        for editable in js_result['editables']:
            print(f"  - Tag: {editable['tag']} | Classes: {editable['classes']} | Placeholder: {editable['placeholder']}")
        
        print("\nMODEL-related elements:")
        for model in js_result['modelElements']:
            print(f"  - Tag: {model['tag']} | Text: '{model['text']}' | Clickable: {model['clickable']}")
        
        print("\n5. NEW CHAT ELEMENTS:")
        new_chat_selectors = [
            'a[href="/new"]',
            'button:contains("New")',
            '[href*="/new"]',
            'button[aria-label*="new"]',
            'button[aria-label*="chat"]'
        ]
        
        for selector in new_chat_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    elem = elements[0]
                    print(f"✓ FOUND NEW CHAT: {selector}")
                    print(f"  - Tag: {elem.tag_name}")
                    print(f"  - Text: {elem.text}")
                    print(f"  - Href: {elem.get_attribute('href')}")
                    print(f"  - Classes: {elem.get_attribute('class')}")
            except:
                pass
        
        print("\n=== ANALYSIS COMPLETE ===")
        print("Use this information to update the selectors in anthropic_client.py")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
    
    finally:
        # Don't close the driver since we're attaching to existing browser
        pass

if __name__ == "__main__":
    print("Make sure Chrome is running with debug port 9222")
    print("Navigate to claude.ai in your browser first")
    input("Press Enter when ready...")
    debug_claude_structure()