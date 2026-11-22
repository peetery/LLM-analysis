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

### Optional efficient analysis

Add `--efficient-analysis` to the CLI experiment command to compile locally,
execute the suite once under branch coverage, and skip HTML generation. This
mode does not discard failing tests: mutation testing runs only when the entire
nonempty suite passes. The default retains the historical filtering workflow.
The mode is recorded in `experiment_results.json`.

Coverage now comes from `coverage.json` in both modes. Statement and branch
percentages use covered/total counts independently, including wholly unexecuted
branches; they are not directly comparable to the older text-parser estimates.
The existing mutmut integration is otherwise unchanged.

`tests/test_order_calculator_contracts.py` contains a compact, manually
source-derived suite for boundary validation, error messages, state changes,
discounted shipping thresholds, and tax on shipping. It does not modify the
application or claim LLM-generated performance. Run the contracts and analysis
regressions with:

```bash
python -m unittest discover -s tests -v
```

### Qwen through OpenRouter

The `qwen3-coder-30b` client uses `qwen/qwen3-coder-30b-a3b-instruct`,
temperature 0.2 and a 6,000-token output cap. It works with both existing
prompting strategies. Generate a fresh suite with:

```bash
python automation/cli_experiment_runner.py \
  --model qwen3-coder-30b --source-file order_calculator.py \
  --class-name OrderCalculator --strategy simple_prompting \
  --context full_context --efficient-analysis --prompt-key \
  --results-dir qwen_results
```

Enter the key at the hidden terminal prompt, or omit `--prompt-key` when
`OPENROUTER_API_KEY` is already set. Credentials are not saved in results.
Provider usage and finish reasons are saved alongside the generated response.
Requests are not automatically retried, and incomplete output or a different
response model is rejected. The manually written contract suite is not included
in the generated suite or used as generation feedback.

Add `--refine-failures` to opt into at most one additional Qwen request when
the initial suite compiles but fails. The repair prompt contains source, tests,
and execution failures, never mutants. Only numeric literals in reported failing
`assertEqual`/`assertAlmostEqual` expectations can change; the AST guard preserves
inputs, actual expressions, methods, other assertions, and tolerances. The entire
candidate must pass with the original test count before acceptance. This narrowly
handles numeric-oracle errors, not arbitrary generation failures.

Original results remain unchanged. The candidate, raw edit response, validation,
and `repair_audit.json` are saved in `refinement_001/`. Accepted oracles still
require review: passing the reference does not independently prove a contract.
The refinement report is validation-only; mutation evaluation must follow
acceptance as a separately reported stage. A failed/rejected repair is retained
for inspection and is never automatically retried.

### Local Gemini demo UI

The existing UI and `run_qwen.py` launcher now generate with **Gemini 3.6 Flash
through Google's native API**, not OpenRouter. Enter a Google AI Studio API key.
Legacy filenames/result directories remain unchanged to minimize the switch.
Gemini cache identities and response provenance are separate from Qwen;
the same reference-test, branch-coverage, and mutation gates still apply.
Gemini generation uses streaming responses with character-count progress.
The network idle timeout is 300 seconds; streams have a 600-second deadline.
Incomplete streams remain blocked, and paid requests are never automatically retried.

For a Google Gemini **key-only** authentication check, run
`python check_gemini_key.py` and enter the key at the hidden Terminal prompt.
It makes a model-list GET request, not a text-generation request. Use
`python check_gemini_key.py --mock` for a dummy-key test with no network;
mock success does not validate a real key or generation quota.

```bash
python qwen_ui.py
```

Open `http://127.0.0.1:8766/`. Select OrderCalculator or, when available beside
this repository, the ShoppingCart sample; alternatively upload/paste a standalone
Python file. Enter an OpenRouter key and click **Run fresh paid Qwen**. Fresh
generation is the default, with one initial request and at most two feedback
requests. The UI shows progress, final reference status, both coverage/mutation
scores, actual model request count, and downloadable tests/reports/model output.

The key is passed in memory through the worker's stdin, never in command
arguments, environment variables, browser storage, URLs or result files.
Only one run can be active. The server binds only to localhost; it validates
the host and uses a per-server token for API requests. Uploaded source and
analysis artifacts persist under `qwen_results/`, but API keys do not.
The same verified backend and honest `blocked` status apply, including for
truncated model output. No target score is guaranteed for fresh generation.

### Verified repeatable Qwen runs

```bash
python run_qwen.py
```

For a live demonstration with fresh **paid LLM generation**, bypass the cache:

```bash
python run_qwen.py --fresh --max-refinements 2
```

This makes one initial Qwen request and allows up to two feedback requests.
It does not load an old test suite, and cannot be combined with resume/replay.
The same quality gates apply; a fresh generation is not guaranteed to qualify.
The final JSON includes branch coverage, mutation score and reference test status.

This launcher requires **mutation >60%** on the entire frozen pool and
**branch coverage >=98%**, with a passing nonempty suite and no skipped tests.
It generates a fixed, deduplicated, compilable mutmut pool, keeps overlapping
source regions together, and uses only development mutants as generation
feedback. Held-out outcomes are evaluated after refinement, never included in
prompts. These are practical fixed source-conformance benchmarks, not a new
blind replication of the publication.

A cache miss permits one initial Qwen request and at most two feedback rounds.
Existing inputs, methods and assertions are preserved; only audited failing
numeric literals may change, and new coverage is added in new test classes
(maximum 16 methods for numeric-repair rounds, preferably grouped into eight or
fewer). Once the suite passes, refinement becomes additions-only: all proposed
edits are rejected and recorded in `admission.json`; up to 32 new methods are
validated together without modifying or dropping original tests or assertions.
`--additions-only` explicitly requires this mode with a passing starting suite.
Failing reference suites use a separate repair-only phase: guarded numeric edits
are validated on all original tests, while every proposed addition is rejected
and retained in the admission audit. New coverage is considered only after the
original suite passes. Direct writes to detected source-instance state, container
mutation and private-method calls are rejected rather than used to force
unreachable coverage. Repair explanations remain pending independent oracle review.
If exact edit text occurs more than once, it is accepted only when the traceback
identifies one unique failing occurrence. Passing duplicates are untouched;
multiple failing matches or absent failure evidence remain rejected.
Candidates must pass reference execution before admission. Targets are quality
gates, not guarantees: exhausted budgets, rejected candidates and low scores
produce `blocked` with exit code 2, never a successful result.

Qualified Qwen suites are cached in `.verified_qwen_cache/`, bound to source,
mutant pool, model settings, thresholds, Python/coverage/mutmut environment and
pipeline code hashes. Repeat runs revalidate the cached suite locally and reuse
the identical mutation evaluation with **zero model requests and no key prompt**.
Changed inputs/environment or modified cache contents cannot reuse old results.
Evidence is saved under `qwen_results/verified/`.

To qualify an existing raw Qwen run without paying for another initial suite:

```bash
python run_qwen.py --resume-from \
  qwen_results/simple_prompting/full_context/qwen3-coder-30b/run_001
```

The resume path must contain a complete Qwen response and the same source.
Manual contract suites and manually repaired suites are not seeded into the
verified Qwen cache. Use `python run_qwen.py path/to/another_module.py` for a new
source; do not reuse a resume path from a different source.

`--resume-from` also accepts a prior verified-mode run with an admitted but
low-scoring suite. Its complete Qwen response lineage is reconstructed and
validated, so previously admitted tests stay intact and initial generation is
not repeated. Add `--max-refinements 1` to permit only one new feedback request
(`0`, `1`, and `2` are supported).

Complete saved Qwen feedback can be revalidated without another model request:
`python run_qwen.py --replay-from path/to/blocked_verified_run`. This validates
source/pool identity and provider metadata, applies only responses matching the
current admitted suite, and never asks for a key. JSON additions may be a string
or a list of complete Python strings; list normalization does not alter test code
or bypass oracle, syntax, name-collision, execution, or quality checks.

A standalone trailing Markdown closing fence after one complete JSON object is
also tolerated. Additional JSON objects, prose and incomplete JSON are rejected.
Generation receives a source-derived branch checklist; feedback prioritizes
exact missing source guards before duplicate or unrelated tests. This improves
coverage targeting but does not guarantee that a fresh LLM response is correct.

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
