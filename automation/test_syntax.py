#!/usr/bin/env python3
try:
    import openai_client
    print("✅ openai_client.py syntax OK")
except SyntaxError as e:
    print(f"❌ Syntax error in openai_client.py: {e}")
except Exception as e:
    print(f"⚠️ Other error: {e}")

try:
    import run_experiments
    print("✅ run_experiments.py syntax OK")
except SyntaxError as e:
    print(f"❌ Syntax error in run_experiments.py: {e}")
except Exception as e:
    print(f"⚠️ Other error: {e}")