# LLM Test Generation Analysis

Experimental framework for evaluating automated unit test generation by Large Language Models. Part of an engineering thesis: *"Impact of Code Context and Prompting Strategies on Automated Unit Test Generation with Modern Large Language Models"*.

## Overview

This system automates 720 experiments comparing 4 LLM models across 2 prompting strategies and 3 code context levels. Each experiment generates a unit test suite for the `OrderCalculator` class, then evaluates it using code coverage, mutation testing, and quality metrics.

### Models Tested (via CLI tools)

| CLI Tool     | Model              | Alias                    |
|-------------|--------------------|--------------------------|
| Claude Code  | Claude Sonnet 4.5  | `claude-code-sonnet-4.5` |
| Claude Code  | Claude Opus 4.5    | `claude-code-opus-4.5`   |
| Gemini CLI   | Gemini 3 Pro       | `gemini-3-pro`           |
| Gemini CLI   | Gemini 3 Flash     | `gemini-3-flash`         |

### Prompting Strategies

- **Simple Prompting** -- single prompt requesting a complete test suite
- **Chain-of-Thought (CoT)** -- 3-step process: analyze, plan, implement

### Code Context Levels

- **Interface** -- method signatures only
- **Interface + Docstring** -- signatures with documentation
- **Full Context** -- complete source code

## Repository Structure

```
LLM-analysis/
├── order_calculator.py                # Class under test
├── automation/
│   ├── cli_automation/                # CLI client implementations
│   │   ├── base_cli_client.py         # Abstract base (subprocess, retry, CoT)
│   │   ├── claude_code_client.py      # Claude Code CLI client
│   │   ├── gemini_cli_client.py       # Gemini CLI client
│   │   └── codex_client.py            # OpenAI Codex CLI client (partial)
│   ├── configs/                       # Model configuration files (JSON)
│   ├── data/                          # Aggregated experiment data
│   │   ├── raw_data.csv               # 720 experiment results
│   │   └── summary_by_config.csv      # Per-configuration summary
│   ├── cli_results/                   # Raw results (720 experiment directories)
│   │   ├── simple_prompting/
│   │   └── chain_of_thought_prompting/
│   ├── cli_experiment_runner.py       # Experiment orchestrator
│   ├── experiment_runner.py           # Analysis pipeline
│   ├── class_context_extractor.py     # AST-based context extraction
│   ├── prompt_strategies.py           # Prompting strategy implementations
│   ├── prompt_templates.py            # Prompt template manager
│   └── streamlit_app.py              # Web interface
├── mutants/                           # Mutation testing configuration (mutmut)
└── _archive/                          # Archived files (not part of the system)
```

## Architecture

### Experiment Pipeline

```
CLI Client (Claude/Gemini)
    → sends prompt (strategy + context level)
    → receives generated test code
    ↓
ExperimentRunner
    → saves test file
    → compilation check (py_compile)
    → test execution (unittest)
    → coverage analysis (coverage.py, branch mode)
    → mutation testing (mutmut, 217 mutants)
    → quality metrics (assertions, naming, independence)
    → saves analysis_results.json
```

### Universal Mode

The system supports testing any Python class via `ClassContextExtractor`, which uses AST parsing to extract class information at different context levels.

## Usage

### Requirements

- Python 3.9+
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) (for Claude models)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) (for Gemini models)
- Dependencies: `pip install coverage streamlit mutmut`

### Run Single Experiment

```bash
cd automation
python cli_experiment_runner.py \
  --model claude-code-sonnet-4.5 \
  --strategy simple_prompting \
  --context full_context
```

### Run with Custom Class (Universal Mode)

```bash
cd automation
python cli_experiment_runner.py \
  --source-file path/to/my_class.py \
  --model gemini-3-pro \
  --strategy chain_of_thought_prompting \
  --context interface_docstring
```

### Web Interface

```bash
cd automation
streamlit run streamlit_app.py
```

### Key Results (720 experiments)

| Model              | Statement Coverage | Branch Coverage | Mutation Score |
|--------------------|--------------------|-----------------|----------------|
| Claude Sonnet 4.5  | 93.7%              | 91.4%           | 35.5%          |
| Claude Opus 4.5    | 93.6%              | 91.1%           | 36.0%          |
| Gemini 3 Flash     | 89.3%              | 87.4%           | 25.0%          |
| Gemini 3 Pro       | 88.8%              | 85.3%           | 26.1%          |

Context level impact on statement coverage: Interface (79.3%) -> Interface+Docstring (96.4%) -> Full Context (98.4%)

## Notes

- Mutation testing requires `fork()` support (Linux/WSL only, not native Windows)
- All 720 experiments are stored in `automation/cli_results/`
- Aggregated data is available in `automation/data/`
