"""
LLM Test Generator - Streamlit Interface

Web interface for automated unit test generation experiments using LLMs.
Supports universal mode (any Python class) and legacy mode (OrderCalculator).

Usage:
    streamlit run streamlit_app.py
"""

import streamlit as st
import subprocess
import sys
import json
import platform
import html
from pathlib import Path
from datetime import datetime

IS_WINDOWS = platform.system() == "Windows"

st.set_page_config(
    page_title="LLM Test Generator",
    page_icon="T",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-dark: #0f1419;
        --bg-card: #1a1f26;
        --bg-input: #242a33;
        --border: #2d3640;
        --text: #e7e9ea;
        --text-dim: #8b98a5;
        --accent: #1d9bf0;
        --accent-hover: #1a8cd8;
        --success: #00ba7c;
        --warning: #ffad1f;
        --error: #f4212e;
    }

    .stApp { background: var(--bg-dark); }

    .main .block-container {
        padding: 1.25rem 2.5rem !important;
        max-width: 1400px;
    }

    #MainMenu, footer, header, [data-testid="stToolbar"],
    .stDeployButton, [data-testid="stDecoration"] { display: none !important; }

    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif !important;
        color: var(--text) !important;
        font-weight: 600 !important;
    }

    p, span, label, div { font-family: 'Inter', sans-serif !important; }
    code, pre { font-family: 'JetBrains Mono', monospace !important; }

    .main-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.25rem;
    }

    .main-subtitle {
        font-size: 0.85rem;
        color: var(--text-dim);
        margin-bottom: 1rem;
    }

    .section-header {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-dim);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.6rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid var(--border);
    }

    .stSelectbox > div > div {
        background: var(--bg-input) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        color: var(--text) !important;
    }

    .stSelectbox label {
        color: var(--text-dim) !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }

    .stRadio > div {
        background: var(--bg-input);
        border-radius: 6px;
        padding: 0.4rem 0.6rem;
    }

    .stRadio label {
        color: var(--text) !important;
        font-size: 0.85rem !important;
    }

    .stTextInput input, .stNumberInput input {
        background: var(--bg-input) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        color: var(--text) !important;
        font-size: 0.85rem !important;
    }

    .stTextInput label, .stNumberInput label {
        font-size: 0.8rem !important;
        color: var(--text-dim) !important;
    }

    .stCheckbox label {
        color: var(--text) !important;
        font-size: 0.85rem !important;
    }

    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        background: var(--accent) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.6rem 1.5rem !important;
        transition: background 0.2s !important;
    }

    .stButton > button:hover { background: var(--accent-hover) !important; }

    .stButton > button:disabled {
        background: var(--bg-input) !important;
        color: var(--text-dim) !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.75rem !important;
        color: var(--text) !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-dim) !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
    }

    .stAlert {
        background: var(--bg-card) !important;
        border-radius: 6px !important;
        padding: 0.6rem 0.75rem !important;
    }

    .stCode, pre {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        font-size: 0.75rem !important;
    }

    .context-label {
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        margin-bottom: 0.5rem !important;
    }

    hr {
        border-color: var(--border) !important;
        margin: 0.75rem 0 !important;
    }

    [data-testid="stFileUploader"] {
        background: var(--bg-card);
        border: 1px dashed var(--border);
        border-radius: 6px;
        padding: 0.6rem;
    }

    [data-testid="InputInstructions"], .stTooltipIcon { display: none !important; }

    .status-success {
        display: inline-block;
        background: rgba(0, 186, 124, 0.2);
        color: var(--success);
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .status-error {
        display: inline-block;
        background: rgba(244, 33, 46, 0.2);
        color: var(--error);
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .results-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1.25rem;
        text-align: center;
    }

    .results-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        font-weight: 600;
        color: var(--text);
    }

    .results-value.good { color: var(--success); }
    .results-value.warning { color: var(--warning); }
    .results-value.muted { color: var(--text-dim); font-size: 1.25rem; }

    .results-label {
        font-size: 0.7rem;
        color: var(--text-dim);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.4rem;
    }

    .results-note {
        font-size: 0.65rem;
        color: var(--text-dim);
        margin-top: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)


def get_available_models():
    """Return available CLI models grouped by provider."""
    return {
        "Claude Code": {
            "claude-code-sonnet-4.5": "Claude Sonnet 4.5",
            "claude-code-opus-4.5": "Claude Opus 4.5",
        },
        "Google Gemini": {
            "gemini-3-pro": "Gemini 3 Pro",
            "gemini-3-flash": "Gemini 3 Flash",
        }
    }


def get_model_display_name(model_id: str) -> str:
    """Get human-readable model name from model ID."""
    models = get_available_models()
    for provider_models in models.values():
        if model_id in provider_models:
            return provider_models[model_id]
    return model_id


def get_class_info(file_path: Path, class_name: str = None):
    """Extract class info using ClassContextExtractor."""
    try:
        from class_context_extractor import ClassContextExtractor
        extractor = ClassContextExtractor(file_path, class_name)
        return extractor.get_class_info()
    except Exception:
        return None


def get_context_preview(file_path: Path, context_level: str, class_name: str = None):
    """Extract context at specified level for preview."""
    try:
        from class_context_extractor import ClassContextExtractor
        extractor = ClassContextExtractor(file_path, class_name)
        return extractor.extract_context(context_level)
    except Exception as e:
        return f"Error: {e}"


def parse_experiment_results(results_dir: str, strategy: str, context: str, model: str) -> dict:
    """Parse experiment results from most recent run."""
    try:
        base_path = Path(results_dir) / strategy / context / model
        if not base_path.exists():
            return None

        runs = sorted(
            [d for d in base_path.iterdir() if d.is_dir() and d.name.startswith("run_")],
            key=lambda x: x.name, reverse=True
        )
        run_dir = runs[0] if runs else base_path

        analysis_file = run_dir / "analysis_results.json"
        if not analysis_file.exists():
            exp_file = run_dir / "experiment_results.json"
            if exp_file.exists():
                with open(exp_file) as f:
                    data = json.load(f)
                return {
                    "statement_coverage": 0,
                    "branch_coverage": 0,
                    "mutation_score": 0,
                    "tests_passed": 0,
                    "tests_failed": 0,
                    "total_tests": 0,
                    "quality_score": 0,
                    "response_time": data.get("response_time", 0),
                    "run_dir": str(run_dir),
                }
            return None

        with open(analysis_file) as f:
            data = json.load(f)

        summary = data.get("summary", {})
        return {
            "statement_coverage": summary.get("statement_coverage", 0),
            "branch_coverage": summary.get("branch_coverage", 0),
            "mutation_score": summary.get("mutation_score", 0),
            "tests_passed": summary.get("tests_passed", 0),
            "tests_failed": summary.get("tests_failed", 0),
            "total_tests": summary.get("tests_generated", 0),
            "quality_score": summary.get("overall_quality_score", 0),
            "response_time": summary.get("response_time", 0),
            "run_dir": str(run_dir),
        }
    except Exception:
        return None


def run_experiment(source_file: str, model: str, strategy: str, context: str,
                   class_name: str = None, run_id: int = None, results_dir: str = None):
    """Run experiment using CLI runner."""
    cmd = [sys.executable, "cli_experiment_runner.py",
           "--model", model, "--strategy", strategy, "--context", context]

    if source_file:
        cmd.extend(["--source-file", source_file])
    if class_name:
        cmd.extend(["--class-name", class_name])
    if run_id:
        cmd.extend(["--run-id", str(run_id)])
    if results_dir:
        cmd.extend(["--results-dir", results_dir])

    return subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, cwd=str(Path(__file__).parent), bufsize=1
    )


def render_config_view():
    """Render the configuration view."""
    st.markdown('<h1 class="main-title">LLM Test Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Automated unit test generation using Large Language Models</p>', unsafe_allow_html=True)

    main_col, side_col = st.columns([2, 1])

    source_file = None
    class_name = None
    class_info = None

    with main_col:
        st.markdown('<div class="section-header">Mode</div>', unsafe_allow_html=True)
        mode = st.radio(
            "Select mode",
            ["Legacy (OrderCalculator)", "Universal (Any Class)"],
            label_visibility="collapsed",
            horizontal=True
        )

        if mode == "Universal (Any Class)":
            st.markdown('<div class="section-header">Source File</div>', unsafe_allow_html=True)
            input_col1, input_col2 = st.columns([2, 1])
            with input_col1:
                source_file = st.text_input("File path", placeholder="path/to/your_class.py", label_visibility="collapsed")
            with input_col2:
                uploaded = st.file_uploader("or upload", type=["py"], label_visibility="collapsed")
                if uploaded:
                    temp = Path(__file__).parent / "temp_upload.py"
                    temp.write_bytes(uploaded.getvalue())
                    source_file = str(temp)

            if source_file and Path(source_file).exists():
                class_info = get_class_info(Path(source_file))
                if class_info:
                    st.success(f"Detected: {class_info.name} ({len(class_info.public_methods)} methods)")
                else:
                    st.warning("Multiple classes found. Specify class name:")
                    class_name = st.text_input("Class name", placeholder="ClassName", label_visibility="collapsed")
                    if class_name:
                        class_info = get_class_info(Path(source_file), class_name)
                        if class_info:
                            st.success(f"Loaded: {class_info.name}")
        else:
            order_path = Path(__file__).parent / "order_calculator.py"
            if order_path.exists():
                class_info = get_class_info(order_path)
                source_file = str(order_path)

        st.markdown("---")

        st.markdown('<div class="section-header">Configuration</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            models = get_available_models()
            provider = st.selectbox("Provider", list(models.keys()))
            model_opts = models[provider]
            selected_model = st.selectbox("Model", list(model_opts.keys()), format_func=lambda x: model_opts[x])

        with col2:
            strategy = st.selectbox(
                "Strategy",
                ["simple_prompting", "chain_of_thought_prompting"],
                format_func=lambda x: "Simple Prompting" if "simple" in x else "Chain-of-Thought"
            )

        with col3:
            context = st.selectbox(
                "Context Level",
                ["interface", "interface_docstring", "full_context"],
                format_func=lambda x: {
                    "interface": "Interface",
                    "interface_docstring": "Interface + Docstrings",
                    "full_context": "Full Implementation"
                }[x]
            )

        st.markdown("---")
        st.markdown('<div class="section-header">Advanced Options</div>', unsafe_allow_html=True)
        adv_col1, adv_col2 = st.columns(2)
        with adv_col1:
            run_id = st.number_input("Run ID (0 = auto)", min_value=0, value=0)
        with adv_col2:
            results_dir = st.text_input("Results directory", value="cli_results")

        st.markdown("---")
        can_run = mode == "Legacy (OrderCalculator)" or (source_file and Path(source_file).exists() and class_info)

        if st.button("Run Experiment", disabled=not can_run, use_container_width=True, type="primary"):
            st.session_state.running = True
            st.session_state.output = []
            st.session_state.config = {
                "mode": mode,
                "source_file": source_file if mode == "Universal (Any Class)" else None,
                "class_name": class_name,
                "model": selected_model,
                "strategy": strategy,
                "context": context,
                "run_id": run_id if run_id > 0 else None,
                "results_dir": results_dir
            }
            st.rerun()

        if IS_WINDOWS:
            st.caption("Windows: Mutation testing unavailable (requires Linux/WSL)")

    with side_col:
        st.markdown('<p class="context-label">Context Preview</p>', unsafe_allow_html=True)

        src = source_file if source_file else str(Path(__file__).parent / "order_calculator.py")
        if src and Path(src).exists() and class_info:
            preview = get_context_preview(Path(src), context, class_name)
            if preview and not preview.startswith("Error"):
                from streamlit.components.v1 import html as st_html
                escaped_code = html.escape(preview)
                html_content = f'''
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
                <style>
                    body {{ margin: 0; padding: 0; background: transparent; }}
                    pre {{ margin: 0; padding: 12px; background: #1a1f26; border-radius: 6px; overflow: auto; font-size: 11px; line-height: 1.5; }}
                    code {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; }}
                </style>
                <pre><code class="language-python">{escaped_code}</code></pre>
                <script>hljs.highlightAll();</script>
                '''
                st_html(html_content, height=500, scrolling=True)
            else:
                st.error(str(preview)[:200])
        else:
            st.info("Select a class to see context preview.")

    return selected_model, strategy, context


def render_running_view():
    """Render the running experiment view."""
    config = st.session_state.config
    model_name = get_model_display_name(config["model"])

    st.markdown(f'<h1 class="main-title">Processing with {model_name}...</h1>', unsafe_allow_html=True)

    console = st.empty()

    process = run_experiment(
        config["source_file"],
        config["model"],
        config["strategy"],
        config["context"],
        config["class_name"],
        config["run_id"],
        config["results_dir"] if config["results_dir"] != "cli_results" else None
    )

    lines = []
    for line in process.stdout:
        lines.append(line.strip())
        console.code("\n".join(lines[-30:]), language="")

    process.wait()
    success = process.returncode == 0

    actual_dir = config["results_dir"] or "cli_results"
    metrics = parse_experiment_results(actual_dir, config["strategy"], config["context"], config["model"])

    st.session_state.running = False
    st.session_state.output = lines
    st.session_state.metrics = metrics
    st.session_state.result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "success": success
    }
    st.rerun()


def render_results_view():
    """Render the results view."""
    config = st.session_state.config
    metrics = st.session_state.metrics
    result = st.session_state.result

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h1 class="main-title">Experiment Results</h1>', unsafe_allow_html=True)
        st.caption(f"Finished at {result['timestamp']}")
    with col2:
        if result["success"]:
            st.markdown('<div style="text-align: right;"><span class="status-success">Completed</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: right;"><span class="status-error">Failed</span></div>', unsafe_allow_html=True)

    if metrics:
        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            stmt = metrics.get("statement_coverage", 0)
            color_class = "good" if stmt >= 80 else ""
            st.markdown(f'''
            <div class="results-card">
                <div class="results-value {color_class}">{stmt:.1f}%</div>
                <div class="results-label">Statement Coverage</div>
            </div>
            ''', unsafe_allow_html=True)

        with col2:
            branch = metrics.get("branch_coverage", 0)
            st.markdown(f'''
            <div class="results-card">
                <div class="results-value">{branch:.1f}%</div>
                <div class="results-label">Branch Coverage</div>
            </div>
            ''', unsafe_allow_html=True)

        with col3:
            mut = metrics.get("mutation_score", 0)
            if IS_WINDOWS and mut == 0:
                st.markdown('''
                <div class="results-card">
                    <div class="results-value muted">N/A</div>
                    <div class="results-label">Mutation Score</div>
                    <div class="results-note">Linux only</div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                color_class = "good" if mut >= 30 else ("warning" if mut >= 15 else "")
                st.markdown(f'''
                <div class="results-card">
                    <div class="results-value {color_class}">{mut:.1f}%</div>
                    <div class="results-label">Mutation Score</div>
                </div>
                ''', unsafe_allow_html=True)

        with col4:
            quality = metrics.get("quality_score", 0)
            st.markdown(f'''
            <div class="results-card">
                <div class="results-value">{quality:.0f}</div>
                <div class="results-label">Quality Score</div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Response Time", f"{metrics.get('response_time', 0):.1f}s")
        with col2:
            st.metric("Test Methods", f"{metrics.get('total_tests', 0)}")
        with col3:
            passed = metrics.get("tests_passed", 0)
            total = metrics.get("total_tests", 0)
            st.metric("Tests Passed", f"{passed}/{total}" if total > 0 else "-")
        with col4:
            st.metric("Tests Failed", f"{metrics.get('tests_failed', 0)}")

    st.markdown("---")
    model_name = get_model_display_name(config["model"])
    strategy_name = "Simple Prompting" if "simple" in config["strategy"] else "Chain-of-Thought"
    context_name = {"interface": "Interface", "interface_docstring": "Interface + Docstrings", "full_context": "Full Implementation"}[config["context"]]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"Model: {model_name}")
    with col2:
        st.caption(f"Strategy: {strategy_name}")
    with col3:
        st.caption(f"Context: {context_name}")

    if st.session_state.output:
        st.markdown("---")
        if st.checkbox("Show console output"):
            st.code("\n".join(st.session_state.output[-100:]), language="")

    st.markdown("---")
    if st.button("Run Another Experiment", use_container_width=True):
        st.session_state.running = False
        st.session_state.result = None
        st.session_state.metrics = None
        st.session_state.output = []
        st.rerun()


def main():
    if "running" not in st.session_state:
        st.session_state.running = False
    if "output" not in st.session_state:
        st.session_state.output = []
    if "result" not in st.session_state:
        st.session_state.result = None
    if "metrics" not in st.session_state:
        st.session_state.metrics = None
    if "config" not in st.session_state:
        st.session_state.config = None

    main_container = st.empty()

    with main_container.container():
        if st.session_state.running:
            render_running_view()
        elif st.session_state.result is not None:
            render_results_view()
        else:
            render_config_view()


if __name__ == "__main__":
    main()
