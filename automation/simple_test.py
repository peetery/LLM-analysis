#!/usr/bin/env python3
import sys
print("Python version:", sys.version)
print("Testing imports...")

try:
    from selenium import webdriver
    print("✅ Selenium import OK")
except ImportError as e:
    print(f"❌ Selenium not found: {e}")

try:
    import time
    import os
    print("✅ Basic imports OK")
except Exception as e:
    print(f"❌ Basic imports failed: {e}")

# Test WSL detection
try:
    with open('/proc/version', 'r') as f:
        version_info = f.read().lower()
        if 'microsoft' in version_info or 'wsl' in version_info:
            print("🐧 WSL detected!")
        else:
            print("🖥️ Linux/Native detected")
except:
    print("❓ Cannot detect environment")