# LLM Test Generation Automation

Automated system for evaluating LLM-generated unit tests using different prompting strategies and code contexts.

## 📁 Directory Structure

```
automation/
├── cli_automation/              # CLI-based automation (subprocess)
│   ├── base_cli_client.py      # Base CLI client
│   ├── claude_code_client.py   # Claude Code CLI client
│   └── gemini_cli_client.py    # Gemini CLI client
├── cli_results/                 # CLI automation results
├── prompts_results/             # Legacy results directory
├── experiment_runner.py         # Analysis pipeline (shared)
├── prompt_strategies.py         # Prompting strategies
├── cli_experiment_runner.py    # CLI automation entry point
├── run_mutmut_backfill.py      # Mutation testing backfill (Windows→WSL)
├── aggregate_runs.py           # Aggregate multiple runs
├── cli_config.json             # CLI automation config
├── gemini_cli_config.json      # Gemini CLI config
└── requirements.txt            # Python dependencies
```

## 🚀 Quick Start

### CLI Automation

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

## 🧪 Mutation Testing

**On Windows:** Mutation testing is automatically skipped (requires fork support).

**Backfill from WSL/Linux:**
```bash
# From WSL
cd /mnt/c/Users/.../LLM-analysis/automation
python3 run_mutmut_backfill.py --results-dir cli_results
```

## 📊 Results Structure

Results are organized in `cli_results/{strategy}/{context}/{model}/run_XXX/`

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

**CLI automation requirements:**
- Claude Code: Already installed (you're using it!)
- Google Gemini: `npm install -g @google/gemini-cli`

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
- Results stay in `cli_results/`

### Mutation Testing
- **Requires WSL/Linux** (fork support needed)
- Use `run_mutmut_backfill.py` to add mutation results later
- Automatically filters to passing tests only

## 📄 License

Research project - see repository root for license.
