# LLM Test Generation Automation

Automated system for evaluating LLM-generated unit tests using different prompting strategies and code contexts.

## 📁 Directory Structure

```
automation/
├── web_automation/              # Web-based automation (Selenium)
│   ├── base_llm_client.py      # Base Selenium client
│   ├── openai_client.py        # ChatGPT automation
│   ├── anthropic_client.py     # Claude.ai automation
│   ├── deepseek_client.py      # DeepSeek automation
│   ├── google_client.py        # Gemini automation
│   └── huggingface_client.py   # HuggingFace automation
├── cli_automation/              # CLI-based automation (subprocess)
│   ├── base_cli_client.py      # Base CLI client
│   └── claude_code_client.py   # Claude Code CLI client
├── docs/                        # Documentation
│   ├── CLI_AUTOMATION.md       # CLI automation guide
│   ├── MUTATION_TESTING.md     # Mutation testing guide
│   ├── WSL_SETUP.md            # WSL configuration
│   ├── WSL_CHROME_SETUP.md     # Chrome debugging setup
│   └── archive/                # Historical documentation
├── prompts_results/             # Web automation results
├── cli_results/                 # CLI automation results
├── experiment_runner.py         # Core experiment orchestration
├── prompt_strategies.py         # Prompting strategies
├── run_experiments.py           # Web automation entry point
├── cli_experiment_runner.py    # CLI automation entry point
├── run_mutmut_backfill.py      # Mutation testing backfill (Windows→WSL)
├── experiment_config.json       # Web automation config
├── cli_config.json             # CLI automation config
└── requirements.txt            # Python dependencies
```

## 🚀 Quick Start

### CLI Automation (Recommended)

**List available models:**
```bash
cd automation
python cli_experiment_runner.py --list-models
```

**Run single experiment:**
```bash
python cli_experiment_runner.py \
  --model claude-code-sonnet-4.5 \
  --strategy simple_prompting \
  --context interface
```

**Run batch experiments:**
```bash
python cli_experiment_runner.py --config cli_config.json
```

See [docs/CLI_AUTOMATION.md](docs/CLI_AUTOMATION.md) for details.

### Web Automation (Legacy)

**Interactive mode:**
```bash
python run_experiments.py
```

**Single experiment:**
```bash
python run_experiments.py \
  --model gpt-4.5 \
  --strategy simple_prompting \
  --context interface \
  --no-headless
```

**Batch experiments:**
```bash
python run_experiments.py --config experiment_config.json --no-headless
```

## 🧪 Mutation Testing

**On Windows:** Mutation testing is automatically skipped (requires fork support).

**Backfill from WSL/Linux:**
```bash
# From WSL
cd /mnt/c/Users/.../LLM-analysis/automation
python3 run_mutmut_backfill.py --results-dir cli_results
```

See [docs/MUTATION_TESTING.md](docs/MUTATION_TESTING.md) for details.

## 📊 Results Structure

Results are organized by automation type:

**Web automation:** `prompts_results/{strategy}/{context}/{model}/`
**CLI automation:** `cli_results/{strategy}/{context}/{model}/`

Each result directory contains:
- `tests.py` - Generated test code
- `mutmut_test.py` - Filtered tests for mutation testing
- `order_calculator.py` - Source code under test
- `experiment_results.json` - Experiment metadata
- `analysis_results.json` - Coverage, mutation, quality metrics
- `podsumowanie-{model}.md` - Human-readable summary
- `htmlcov/` - Coverage report

## 🔧 Prompting Strategies

**Simple Prompting:** Single prompt requesting tests
**Chain of Thought:** Three-step process (analyze → plan → implement)

## 📝 Context Levels

- **interface:** Method signatures only
- **interface_docstring:** Signatures + docstrings
- **full_context:** Complete implementation

## 🛠️ Development

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Web automation requirements:**
- Chrome with remote debugging (`--remote-debugging-port=9222`)
- Active browser sessions with logged-in LLM accounts

**CLI automation requirements:**
- Claude Code: Already installed (you're using it!)
- OpenAI Codex: `npm install -g @openai/codex`
- GitHub Copilot: `npm install -g @github/copilot`
- Google Gemini: `npm install -g @google/gemini-cli`

## 📚 Documentation

- [CLI Automation Guide](docs/CLI_AUTOMATION.md)
- [Mutation Testing Guide](docs/MUTATION_TESTING.md)
- [WSL Setup](docs/WSL_SETUP.md)
- [Chrome Debug Setup](docs/WSL_CHROME_SETUP.md)
- [Historical Documentation](docs/archive/)

## 🎯 Research Metrics

The system automatically measures:
- **Compilation success rate**
- **Statement coverage** (line coverage)
- **Branch coverage** (decision coverage)
- **Mutation score** (% mutants killed)
- **Test count** (methods generated)
- **Test success rate** (passing vs total)
- **Test quality metrics** (assertions, error handling, duplicates)
- **Code smells** (independence, naming, complexity)

All metrics saved in JSON, CSV, and Markdown formats.

## ⚠️ Important Notes

### File Locations
- Run all scripts from `automation/` directory
- `order_calculator.py` is in repository root
- Results stay in `prompts_results/` and `cli_results/`

### Mutation Testing
- **Requires WSL/Linux** (fork support needed)
- Use `run_mutmut_backfill.py` to add mutation results later
- Automatically filters to passing tests only

### Web Automation
- Always use `--no-headless` for monitoring
- Login state persists across experiments
- Manual intervention possible during execution

## 📄 License

Research project - see repository root for license.
