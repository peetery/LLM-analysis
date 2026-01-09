"""
LLM Test Generation Console - Streamlit Interface

A refined research interface for automated unit test generation experiments.
Supports universal mode (any Python class) and legacy mode (OrderCalculator).

Usage:
    streamlit run streamlit_app.py
"""

import streamlit as st
import subprocess
import sys
import json
import time
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="LLM Test Generator",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=DM+Sans:wght@400;500;600;700&display=swap');

    :root {
        --bg-primary: #12141a;
        --bg-secondary: #1a1d24;
        --bg-tertiary: #22262f;
        --border-color: #2d323c;
        --text-primary: #e8e9eb;
        --text-secondary: #9ca3af;
        --text-muted: #6b7280;
        --accent-gold: #d4a84b;
        --accent-gold-dim: #a68638;
        --accent-green: #4ade80;
        --accent-red: #f87171;
        --accent-blue: #60a5fa;
    }

    .stApp {
        background: var(--bg-primary);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    [data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
        min-width: 340px !important;
        width: 340px !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
        width: 340px !important;
    }

    [data-testid="stToolbar"] { display: none !important; }
    .stDeployButton { display: none !important; }

    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    button[aria-label="Close sidebar"],
    button[aria-label="Open sidebar"],
    .st-emotion-cache-1egp75f {
        display: none !important;
    }

    [data-testid="stSidebar"] {
        transform: none !important;
        position: relative !important;
    }

    [data-testid="stSidebar"][aria-expanded="false"] {
        display: block !important;
        transform: none !important;
        margin-left: 0 !important;
    }

    [data-testid="stSidebar"] [aria-label*="keyboard"],
    [data-testid="stSidebar"] [aria-label*="Keyboard"],
    [data-testid="stSidebar"] button[kind="header"],
    [data-testid="stSidebar"] [data-testid="baseButton-header"] {
        display: none !important;
    }

    .help-section {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        margin-top: 1rem;
        overflow: hidden;
    }

    .help-section summary {
        padding: 0.75rem 1rem;
        cursor: pointer;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        color: var(--text-secondary);
        list-style: none;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .help-section summary::-webkit-details-marker {
        display: none;
    }

    .help-section summary::before {
        content: '+';
        font-family: 'JetBrains Mono', monospace;
        color: var(--accent-gold);
    }

    .help-section[open] summary::before {
        content: '-';
    }

    .help-content {
        padding: 0 1rem 1rem 1rem;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }

    .help-content p {
        margin: 0.5rem 0 0.25rem 0;
        color: var(--text-primary);
    }

    .help-content ul {
        margin: 0;
        padding-left: 1.25rem;
    }

    .help-content li {
        margin: 0.15rem 0;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'DM Sans', sans-serif !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }

    p, span, label, .stMarkdown {
        font-family: 'DM Sans', sans-serif !important;
        color: var(--text-secondary) !important;
    }

    code, pre, .stCode {
        font-family: 'JetBrains Mono', monospace !important;
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
    }

    .console-header {
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }

    .console-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-gold) 0%, var(--accent-gold-dim) 50%, transparent 100%);
    }

    .console-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
        letter-spacing: -0.02em;
    }

    .console-subtitle {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: var(--text-muted);
        margin-top: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .config-section {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }

    .section-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--accent-gold);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 0.75rem;
        display: block;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 500;
    }

    .status-ready {
        background: rgba(74, 222, 128, 0.1);
        color: var(--accent-green);
        border: 1px solid rgba(74, 222, 128, 0.3);
    }

    .status-running {
        background: rgba(212, 168, 75, 0.1);
        color: var(--accent-gold);
        border: 1px solid rgba(212, 168, 75, 0.3);
    }

    .status-error {
        background: rgba(248, 113, 113, 0.1);
        color: var(--accent-red);
        border: 1px solid rgba(248, 113, 113, 0.3);
    }

    .info-card {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }

    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 0.4rem 0;
        border-bottom: 1px solid var(--border-color);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
    }

    .info-row:last-child {
        border-bottom: none;
    }

    .info-label {
        color: var(--text-muted);
    }

    .info-value {
        color: var(--text-primary);
        font-weight: 500;
    }

    .info-value.highlight {
        color: var(--accent-gold);
    }

    .stButton > button {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-gold-dim) 100%) !important;
        color: var(--bg-primary) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.2s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(212, 168, 75, 0.3) !important;
    }

    .stButton > button:disabled {
        background: var(--bg-tertiary) !important;
        color: var(--text-muted) !important;
    }

    .stSelectbox > div > div {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    .stSelectbox label {
        font-family: 'DM Sans', sans-serif !important;
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
    }

    [data-testid="stFileUploader"] {
        background: var(--bg-tertiary);
        border: 2px dashed var(--border-color);
        border-radius: 10px;
        padding: 1rem;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent-gold-dim);
    }

    .stRadio > div {
        background: var(--bg-tertiary);
        border-radius: 8px;
        padding: 0.5rem;
    }

    .stRadio label {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
    }

    .streamlit-expanderHeader {
        font-family: 'DM Sans', sans-serif !important;
        background: var(--bg-tertiary) !important;
        border-radius: 8px !important;
    }

    .stProgress > div > div {
        background: var(--accent-gold) !important;
    }

    .stTextInput input {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: var(--accent-gold) !important;
    }

    [data-testid="stMetricLabel"] {
        font-family: 'DM Sans', sans-serif !important;
        color: var(--text-secondary) !important;
    }

    hr {
        border-color: var(--border-color) !important;
        margin: 1.5rem 0 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary);
        border-radius: 8px;
        padding: 0.25rem;
        gap: 0.25rem;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500;
        color: var(--text-secondary);
        background: transparent;
        border-radius: 6px;
    }

    .stTabs [aria-selected="true"] {
        background: var(--bg-tertiary) !important;
        color: var(--accent-gold) !important;
    }

    .console-output {
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: var(--text-secondary);
        max-height: 400px;
        overflow-y: auto;
        white-space: pre-wrap;
    }

    .console-output .log-info { color: var(--accent-blue); }
    .console-output .log-success { color: var(--accent-green); }
    .console-output .log-warning { color: var(--accent-gold); }
    .console-output .log-error { color: var(--accent-red); }

    .results-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }

    .result-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1.25rem;
        text-align: center;
    }

    .result-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        font-weight: 600;
        color: var(--accent-gold);
    }

    .result-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.85rem;
        color: var(--text-muted);
        margin-top: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)


def get_available_models():
    """Return available CLI models."""
    return {
        "Claude Code": {
            "claude-code-sonnet-4.5": "Sonnet 4.5",
            "claude-code-opus-4.5": "Opus 4.5",
        },
        "Google Gemini": {
            "gemini-3-pro": "Gemini 3 Pro",
            "gemini-3-flash": "Gemini 3 Flash",
        }
    }


def get_class_info(file_path: Path, class_name: str = None):
    """Extract class info using ClassContextExtractor."""
    try:
        from class_context_extractor import ClassContextExtractor
        extractor = ClassContextExtractor(file_path, class_name)
        return extractor.get_class_info()
    except Exception as e:
        return None


def run_experiment(source_file: str, model: str, strategy: str, context: str,
                   class_name: str = None, run_id: int = None):
    """Run experiment using CLI runner."""
    cmd = [
        sys.executable, "cli_experiment_runner.py",
        "--model", model,
        "--strategy", strategy,
        "--context", context
    ]

    if source_file:
        cmd.extend(["--source-file", source_file])
    if class_name:
        cmd.extend(["--class-name", class_name])
    if run_id:
        cmd.extend(["--run-id", str(run_id)])

    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=str(Path(__file__).parent),
        bufsize=1
    )


def render_header():
    """Render the console header."""
    st.markdown("""
    <div class="console-header">
        <h1 class="console-title">LLM Test Generator</h1>
        <p class="console-subtitle">Automated Unit Test Generation Console</p>
    </div>
    """, unsafe_allow_html=True)


def render_class_info(info):
    """Render class information card."""
    if info:
        helper_types = ", ".join(info.helper_types) if info.helper_types else "None"
        st.markdown(f"""
        <div class="info-card">
            <div class="info-row">
                <span class="info-label">Class</span>
                <span class="info-value highlight">{info.name}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Module</span>
                <span class="info-value">{info.module_name}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Methods</span>
                <span class="info-value">{len(info.public_methods)}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Helper Types</span>
                <span class="info-value">{helper_types}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_status(status: str):
    """Render status badge."""
    status_classes = {
        "ready": "status-ready",
        "running": "status-running",
        "error": "status-error"
    }
    icons = {
        "ready": "",
        "running": "",
        "error": ""
    }
    st.markdown(f"""
    <span class="status-badge {status_classes.get(status, 'status-ready')}">
        {icons.get(status, '')} {status.upper()}
    </span>
    """, unsafe_allow_html=True)


def main():
    if "experiment_running" not in st.session_state:
        st.session_state.experiment_running = False
    if "experiment_output" not in st.session_state:
        st.session_state.experiment_output = []
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

    render_header()

    with st.sidebar:
        st.markdown('<span class="section-label">Configuration</span>', unsafe_allow_html=True)

        mode = st.radio(
            "Mode",
            ["Universal (Any Class)", "Legacy (OrderCalculator)"],
            help="Universal mode works with any Python class"
        )

        st.divider()

        source_file = None
        class_name = None
        class_info = None

        if mode == "Universal (Any Class)":
            st.markdown('<span class="section-label">Source File</span>', unsafe_allow_html=True)

            file_input_method = st.radio(
                "Input method",
                ["Enter path", "Browse files"],
                horizontal=True,
                label_visibility="collapsed"
            )

            if file_input_method == "Enter path":
                source_file = st.text_input(
                    "Python file path",
                    placeholder="path/to/your_class.py",
                    label_visibility="collapsed"
                )
            else:
                uploaded = st.file_uploader(
                    "Upload Python file",
                    type=["py"],
                    label_visibility="collapsed"
                )
                if uploaded:
                    temp_path = Path(__file__).parent / "temp_upload.py"
                    temp_path.write_bytes(uploaded.getvalue())
                    source_file = str(temp_path)

            if source_file and Path(source_file).exists():
                class_info = get_class_info(Path(source_file))
                if class_info:
                    st.markdown('<span class="section-label">Detected Class</span>',
                               unsafe_allow_html=True)
                    render_class_info(class_info)
                else:
                    class_name = st.text_input(
                        "Class name (multiple classes detected)",
                        placeholder="ClassName"
                    )
                    if class_name:
                        class_info = get_class_info(Path(source_file), class_name)
                        if class_info:
                            render_class_info(class_info)
        else:
            order_calc_path = Path(__file__).parent / "order_calculator.py"
            if order_calc_path.exists():
                class_info = get_class_info(order_calc_path)
                st.markdown('<span class="section-label">Target Class</span>',
                           unsafe_allow_html=True)
                render_class_info(class_info)

        st.divider()

        st.markdown('<span class="section-label">Model</span>', unsafe_allow_html=True)
        models = get_available_models()

        model_provider = st.selectbox(
            "Provider",
            list(models.keys()),
            label_visibility="collapsed"
        )

        model_options = models[model_provider]
        selected_model = st.selectbox(
            "Model",
            list(model_options.keys()),
            format_func=lambda x: model_options[x],
            label_visibility="collapsed"
        )

        st.divider()

        st.markdown('<span class="section-label">Prompting Strategy</span>',
                   unsafe_allow_html=True)
        strategy = st.selectbox(
            "Strategy",
            ["simple_prompting", "chain_of_thought_prompting"],
            format_func=lambda x: {
                "simple_prompting": "Simple (single prompt)",
                "chain_of_thought_prompting": "Chain-of-Thought (3-step)"
            }[x],
            label_visibility="collapsed"
        )

        st.divider()

        st.markdown('<span class="section-label">Context Level</span>',
                   unsafe_allow_html=True)
        context = st.selectbox(
            "Context",
            ["interface", "interface_docstring", "full_context"],
            format_func=lambda x: {
                "interface": "Interface (signatures only)",
                "interface_docstring": "Interface + Docstrings",
                "full_context": "Full Implementation"
            }[x],
            label_visibility="collapsed"
        )

        st.divider()

        st.markdown('<span class="section-label">Run Options</span>',
                   unsafe_allow_html=True)
        run_id = st.number_input("Run ID (auto if 0)", min_value=0, value=0)

        st.divider()

        can_run = (mode == "Legacy (OrderCalculator)" or
                   (source_file and Path(source_file).exists() and class_info))

        if st.button("Run Experiment", disabled=not can_run or st.session_state.experiment_running,
                    use_container_width=True):
            st.session_state.experiment_running = True
            st.session_state.experiment_output = []
            st.rerun()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<span class="section-label">Experiment Status</span>',
                   unsafe_allow_html=True)

        status_col1, status_col2 = st.columns([1, 3])
        with status_col1:
            if st.session_state.experiment_running:
                render_status("running")
            elif st.session_state.last_result:
                render_status("ready")
            else:
                render_status("ready")

        with status_col2:
            if st.session_state.experiment_running:
                st.caption("Experiment in progress...")
            elif st.session_state.last_result:
                st.caption(f"Last run: {st.session_state.last_result.get('timestamp', 'N/A')}")
            else:
                st.caption("Configure and run an experiment")

        st.markdown('<span class="section-label">Console Output</span>',
                   unsafe_allow_html=True)

        output_container = st.container()

        if st.session_state.experiment_running:
            with st.spinner("Running experiment..."):
                process = run_experiment(
                    source_file if mode == "Universal (Any Class)" else None,
                    selected_model,
                    strategy,
                    context,
                    class_name,
                    run_id if run_id > 0 else None
                )

                output_lines = []
                for line in process.stdout:
                    output_lines.append(line.strip())
                    with output_container:
                        st.code("\n".join(output_lines[-50:]), language="")

                process.wait()

                st.session_state.experiment_running = False
                st.session_state.experiment_output = output_lines
                st.session_state.last_result = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "model": selected_model,
                    "strategy": strategy,
                    "context": context,
                    "success": process.returncode == 0
                }
                st.rerun()
        else:
            with output_container:
                if st.session_state.experiment_output:
                    st.code("\n".join(st.session_state.experiment_output[-50:]), language="")
                else:
                    st.code("No output yet. Run an experiment to see results.", language="")

    with col2:
        st.markdown('<span class="section-label">Configuration Summary</span>',
                   unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-card">
            <div class="info-row">
                <span class="info-label">Mode</span>
                <span class="info-value">{"Universal" if mode.startswith("Universal") else "Legacy"}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Model</span>
                <span class="info-value highlight">{selected_model.split('-')[-1].title()}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Strategy</span>
                <span class="info-value">{"Simple" if "simple" in strategy else "CoT"}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Context</span>
                <span class="info-value">{context.replace("_", " ").title()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.last_result:
            st.markdown('<span class="section-label">Last Run</span>',
                       unsafe_allow_html=True)

            result = st.session_state.last_result
            st.markdown(f"""
            <div class="info-card">
                <div class="info-row">
                    <span class="info-label">Time</span>
                    <span class="info-value">{result.get('timestamp', 'N/A')}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Status</span>
                    <span class="info-value {'highlight' if result.get('success') else ''}"
                          style="color: {'var(--accent-green)' if result.get('success') else 'var(--accent-red)'}">
                        {'Success' if result.get('success') else 'Failed'}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <details class="help-section">
            <summary>Help</summary>
            <div class="help-content">
                <p><strong>Modes:</strong></p>
                <ul>
                    <li><strong>Universal</strong> - Test any Python class</li>
                    <li><strong>Legacy</strong> - Uses OrderCalculator</li>
                </ul>
                <p><strong>Strategies:</strong></p>
                <ul>
                    <li><strong>Simple</strong> - Single prompt</li>
                    <li><strong>CoT</strong> - 3-step process</li>
                </ul>
                <p><strong>Context:</strong></p>
                <ul>
                    <li><strong>Interface</strong> - Signatures only</li>
                    <li><strong>+ Docstrings</strong> - With docs</li>
                    <li><strong>Full</strong> - Complete code</li>
                </ul>
            </div>
        </details>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
