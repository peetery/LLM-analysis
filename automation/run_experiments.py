#!/usr/bin/env python3
"""
Skrypt uruchamiający eksperymenty LLM
"""
import argparse
import logging
import json
from pathlib import Path
from experiment_runner import ExperimentRunner


def setup_logging():
    """Konfiguracja logowania"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('automation.log'),
            logging.StreamHandler()
        ]
    )


def start_chrome_for_debug():
    """Start Chrome with remote debugging (obsługuje WSL z poprawkami katalogów)"""
    import subprocess
    import time
    import os

    # Sprawdź czy jesteśmy w WSL
    def is_wsl():
        try:
            with open('/proc/version', 'r') as f:
                return 'microsoft' in f.read().lower() or 'wsl' in f.read().lower()
        except:
            return False

    def create_chrome_data_dir():
        """Tworzy katalog danych Chrome z odpowiednimi uprawnieniami"""
        if is_wsl():
            # W WSL użyj katalogu w przestrzeni WSL zamiast Windows
            wsl_temp_dir = "/tmp/chrome_debug_wsl"
            try:
                os.makedirs(wsl_temp_dir, exist_ok=True)
                os.chmod(wsl_temp_dir, 0o755)
                print(f"✓ Created WSL Chrome data directory: {wsl_temp_dir}")
                return wsl_temp_dir
            except Exception as e:
                print(f"⚠️  Failed to create WSL directory: {e}")

                # Fallback: spróbuj Windows temp ale z utworzeniem katalogu
                windows_temp = "/mnt/c/temp/chrome_debug"
                try:
                    # Utwórz katalog przez Windows cmd
                    subprocess.run([
                        "cmd.exe", "/c", "mkdir", "C:\\temp\\chrome_debug"
                    ], capture_output=True)

                    if os.path.exists(windows_temp):
                        print(f"✓ Created Windows temp directory: {windows_temp}")
                        return windows_temp
                except:
                    pass

                # Last resort: użyj katalogu domowego
                home_dir = os.path.expanduser("~/chrome_debug_temp")
                os.makedirs(home_dir, exist_ok=True)
                print(f"✓ Using home directory: {home_dir}")
                return home_dir
        else:
            # Windows/Linux native
            temp_dir = "C:\\temp\\chrome_debug"
            try:
                os.makedirs(temp_dir, exist_ok=True)
                return temp_dir
            except:
                # Fallback do katalogu tymczasowego
                import tempfile
                temp_dir = os.path.join(tempfile.gettempdir(), "chrome_debug")
                os.makedirs(temp_dir, exist_ok=True)
                return temp_dir

    if is_wsl():
        print("🐧 WSL detected - starting Windows Chrome from WSL")
        # W WSL używaj Chrome z Windows
        chrome_paths = [
            '/mnt/c/Program Files/Google/Chrome/Application/chrome.exe',
            '/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        ]

        chrome_path = None
        for path in chrome_paths:
            if os.path.exists(path):
                chrome_path = path
                break

        if not chrome_path:
            print("❌ Chrome not found in Windows from WSL")
            return False

        # Utwórz katalog danych
        data_dir = create_chrome_data_dir()

        cmd = [
            chrome_path,
            "--remote-debugging-port=9222",
            f"--user-data-dir={data_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-default-apps"
        ]

    else:
        # Windows/Linux native
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        data_dir = create_chrome_data_dir()

        cmd = [
            chrome_path,
            "--remote-debugging-port=9222",
            f"--user-data-dir={data_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-default-apps"
        ]

    try:
        # Uruchom Chrome w tle
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

        if is_wsl():
            print("✓ Windows Chrome started from WSL with remote debugging on port 9222")
            print("📝 Automation will connect via WSL → Windows bridge")
            print(f"📁 Data directory: {data_dir}")
        else:
            print("✓ Chrome started with remote debugging on port 9222")
            print("📝 Empty browser opened - ready for automation")
            print(f"📁 Data directory: {data_dir}")

        time.sleep(3)  # Give Chrome time to start
        return True

    except Exception as e:
        print(f"✗ Error starting Chrome: {e}")
        print("💡 Try running: sudo apt update && sudo apt install -y google-chrome-stable")
        return False


def get_model_url(model_name):
    """Get the URL for specific model with direct model selection"""
    model_urls = {
        'gpt-4.5': 'https://chatgpt.com/?model=gpt-4.5',
        'gpt-o3': 'https://chatgpt.com/?model=o3',
        'gpt-o4-mini-high': 'https://chatgpt.com/?model=gpt-4o-mini',
        'claude-3.7-sonnet': 'https://claude.ai/',
        'deepseek': 'https://chat.deepseek.com/',
        'gemini-2.5-pro': 'https://gemini.google.com/'
    }
    return model_urls.get(model_name, 'https://google.com')


def interactive_mode(runner):
    """Interactive mode"""
    print("\n" + "=" * 50)
    print("🤖 LLM TESTING AUTOMATION")
    print("=" * 50)

    # Sprawdź czy jesteśmy w WSL
    def is_wsl():
        try:
            with open('/proc/version', 'r') as f:
                return 'microsoft' in f.read().lower() or 'wsl' in f.read().lower()
        except:
            return False

    wsl_detected = is_wsl()
    if wsl_detected:
        print("\n🐧 WSL DETECTED - Enhanced WSL Support Enabled")

    # Step 1: Browser setup
    print("\n📱 STEP 1: Browser setup")
    if wsl_detected:
        print("1. Start Windows Chrome from WSL (recommended)")
        print("2. I have Chrome debug already running")
    else:
        print("1. Start new Chrome with debug")
        print("2. I have Chrome debug already running")

    try:
        browser_choice = input("\nChoice (1-2): ").strip()

        if browser_choice == "1":
            if not start_chrome_for_debug():
                print("✗ Failed to start Chrome")
                return
        elif browser_choice == "2":
            print("✓ Using existing debug browser")
        else:
            print("✗ Invalid choice")
            return

        # Step 2: Model selection
        print("\n🧠 STEP 2: Model selection")
        models = [
            'gpt-4.5', 'gpt-o3', 'gpt-o4-mini-high',
            'claude-3.7-sonnet', 'deepseek', 'gemini-2.5-pro'
        ]

        for i, model in enumerate(models, 1):
            print(f"{i}. {model}")

        model_choice = int(input("\nSelect model (1-6): ")) - 1
        if model_choice < 0 or model_choice >= len(models):
            raise ValueError("Invalid model choice")

        # Step 3: Strategy
        print("\n🎯 STEP 3: Prompting strategy")
        strategies = ['simple_prompting', 'chain_of_thought_prompting']
        for i, strategy in enumerate(strategies, 1):
            print(f"{i}. {strategy.replace('_', ' ').title()}")

        strategy_choice = int(input("\nSelect strategy (1-2): ")) - 1
        if strategy_choice < 0 or strategy_choice >= len(strategies):
            raise ValueError("Invalid strategy")

        # Step 4: Context
        print("\n📋 STEP 4: Code context level")
        contexts = ['interface', 'interface_docstring', 'full_context']
        context_descriptions = [
            'Interface - method signatures only',
            'Interface + Docstring - signatures with documentation',
            'Full Context - complete source code'
        ]

        for i, (context, desc) in enumerate(zip(contexts, context_descriptions), 1):
            print(f"{i}. {desc}")

        context_choice = int(input("\nSelect context (1-3): ")) - 1
        if context_choice < 0 or context_choice >= len(contexts):
            raise ValueError("Invalid context")

        # Summary
        selected_model = models[model_choice]
        selected_strategy = strategies[strategy_choice]
        selected_context = contexts[context_choice]

        print("\n" + "=" * 50)
        print("📊 EXPERIMENT SUMMARY")
        print("=" * 50)
        print(f"🧠 Model: {selected_model}")
        print(f"🎯 Strategy: {selected_strategy.replace('_', ' ').title()}")
        print(f"📋 Context: {selected_context}")
        print(f"🌐 URL: {get_model_url(selected_model)}")
        print(f"🔍 Model verification: Enhanced model checking enabled")

        if wsl_detected:
            print("🐧 Platform: WSL (Windows Subsystem for Linux)")
            print("🔗 Mode: WSL → Windows Chrome bridge")
        else:
            print("🔗 Mode: Attach to existing browser")

        confirm = input("\n🚀 Run experiment? (y/N): ").strip().lower()

        if confirm != 'y':
            print("❌ Cancelled")
            return

        # Execution
        print("\n🚀 STARTING EXPERIMENT...")
        print("-" * 50)

        # Always use attach mode now
        use_headless = False

        result = runner.run_single_experiment(
            selected_model, selected_strategy, selected_context,
            headless=use_headless
        )

        # Results
        print("\n" + "=" * 50)
        if result:
            print("✅ EXPERIMENT COMPLETED SUCCESSFULLY!")
            print("=" * 50)

            if 'analysis' in result and result['analysis']:
                analysis = result['analysis']

                if 'compilation_success' in analysis:
                    status = "✅ SUCCESS" if analysis['compilation_success'] else "❌ FAILED"
                    print(f"🔧 Compilation: {status}")

                if 'coverage' in analysis and analysis['coverage']:
                    cov = analysis['coverage']
                    coverage_pct = cov.get('coverage_percent', 0)
                    print(f"📊 Code coverage: {coverage_pct}%")

                if 'scenarios' in analysis and analysis['scenarios']:
                    scen = analysis['scenarios']
                    test_count = scen.get('total_test_methods', 0)
                    print(f"🧪 Test count: {test_count}")

                print(f"\n📁 Results saved in: prompts_results/{selected_strategy}/{selected_context}/{selected_model}/")
        else:
            print("❌ EXPERIMENT FAILED!")
            print("=" * 50)
            print("🔍 Check logs in automation.log")

    except (ValueError, KeyboardInterrupt) as e:
        print(f"\n❌ Error: {e}")
        print("🚪 Exiting...")
        return
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return


def main():
    """Główna funkcja"""
    parser = argparse.ArgumentParser(description='LLM Testing Automation')
    parser.add_argument('--model', help='Model name (gpt-4.5, claude-3.7-sonnet, etc.)')
    parser.add_argument('--strategy', choices=['simple_prompting', 'chain_of_thought_prompting'],
                        help='Prompting strategy')
    parser.add_argument('--context', choices=['interface', 'interface_docstring', 'full_context'],
                        help='Code context level')
    parser.add_argument('--config', help='JSON config file for batch experiments')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    parser.add_argument('--no-headless', action='store_true', help='Run browser with GUI (default)')

    args = parser.parse_args()

    setup_logging()
    logger = logging.getLogger(__name__)

    runner = ExperimentRunner()

    # Określ tryb przeglądarki
    headless = args.headless if args.headless else not args.no_headless
    if not args.headless and not args.no_headless:
        headless = False  # Domyślnie GUI dla łatwiejszego debugowania

    if args.config:
        # Batch mode
        logger.info(f"Running batch experiments from {args.config}")
        results = runner.run_batch_experiments(args.config)

        # Zapisz wyniki batch
        batch_results_file = Path("batch_results.json")
        with open(batch_results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        logger.info(f"Batch results saved to {batch_results_file}")

    elif args.model and args.strategy and args.context:
        # Single experiment mode
        logger.info(f"Running single experiment: {args.model} - {args.strategy} - {args.context}")

        result = runner.run_single_experiment(
            args.model, args.strategy, args.context, headless=headless
        )

        if result:
            logger.info("Experiment completed successfully")
            print("\n=== EXPERIMENT RESULTS ===")
            print(f"Model: {args.model}")
            print(f"Strategy: {args.strategy}")
            print(f"Context: {args.context}")

            if 'analysis' in result and result['analysis']:
                analysis = result['analysis']
                if 'compilation_success' in analysis:
                    print(f"Compilation: {'✓' if analysis['compilation_success'] else '✗'}")

                if 'coverage' in analysis and analysis['coverage']:
                    cov = analysis['coverage']
                    print(f"Coverage: {cov.get('coverage_percent', 'N/A')}%")

                if 'scenarios' in analysis and analysis['scenarios']:
                    scen = analysis['scenarios']
                    print(f"Test methods: {scen.get('total_test_methods', 'N/A')}")
        else:
            logger.error("Experiment failed")

    else:
        # Interactive mode
        interactive_mode(runner)


if __name__ == "__main__":
    main()