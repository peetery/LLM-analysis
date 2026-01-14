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
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    /* Fix Material Icons displaying as text */
    [data-testid="stIconMaterial"],
    .st-emotion-cache-4si8ij,
    span[translate="no"][class*="st-emotion-cache"] {
        font-family: 'Material Icons', 'Material Symbols Rounded', sans-serif !important;
        font-feature-settings: 'liga' !important;
        -webkit-font-feature-settings: 'liga' !important;
        -webkit-font-smoothing: antialiased !important;
        text-rendering: optimizeLegibility !important;
        -moz-osx-font-smoothing: grayscale !important;
        font-style: normal !important;
        font-weight: normal !important;
        font-size: 24px !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
    }

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

    /* Hide unnecessary UI elements */
    [data-testid="stHeaderActionElements"],
    [data-testid="InputInstructions"],
    [data-testid="baseButton-header"],
    button[kind="header"],
    kbd,
    .kbd,
    .stTooltipIcon,
    [data-testid="stTooltipIcon"] {
        display: none !important;
    }

    /* Hide input instructions (keyboard shortcuts hints) */
    .stTextInput [class*="InputInstructions"],
    .stNumberInput [class*="InputInstructions"],
    [data-testid="stTextInput"] [data-testid="InputInstructions"],
    [data-testid="stNumberInput"] [data-testid="InputInstructions"] {
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

    /* Pipeline Progress Visualization */
    .pipeline-container {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .pipeline-header {
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .pipeline-steps {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .pipeline-step {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem 1rem;
        background: var(--bg-tertiary);
        border-radius: 8px;
        border: 1px solid transparent;
        transition: all 0.3s ease;
    }

    .pipeline-step.pending {
        opacity: 0.5;
    }

    .pipeline-step.active {
        border-color: var(--accent-gold);
        background: linear-gradient(135deg, rgba(212, 168, 75, 0.1) 0%, var(--bg-tertiary) 100%);
        animation: pulse-border 2s infinite;
    }

    .pipeline-step.completed {
        border-color: var(--accent-green);
        background: linear-gradient(135deg, rgba(74, 222, 128, 0.05) 0%, var(--bg-tertiary) 100%);
    }

    .pipeline-step.error {
        border-color: var(--accent-red);
        background: linear-gradient(135deg, rgba(248, 113, 113, 0.1) 0%, var(--bg-tertiary) 100%);
    }

    @keyframes pulse-border {
        0%, 100% { box-shadow: 0 0 0 0 rgba(212, 168, 75, 0.4); }
        50% { box-shadow: 0 0 0 4px rgba(212, 168, 75, 0.1); }
    }

    .step-icon {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
        flex-shrink: 0;
        transition: all 0.3s ease;
    }

    .step-icon.pending {
        background: var(--bg-primary);
        color: var(--text-muted);
        border: 2px solid var(--border-color);
    }

    .step-icon.active {
        background: var(--accent-gold);
        color: var(--bg-primary);
        border: 2px solid var(--accent-gold);
        animation: spin 1.5s linear infinite;
    }

    .step-icon.completed {
        background: var(--accent-green);
        color: var(--bg-primary);
        border: 2px solid var(--accent-green);
    }

    .step-icon.error {
        background: var(--accent-red);
        color: white;
        border: 2px solid var(--accent-red);
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .step-content {
        flex: 1;
    }

    .step-name {
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        color: var(--text-primary);
        font-size: 0.9rem;
    }

    .step-status {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-top: 0.15rem;
    }

    .step-time {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: var(--text-muted);
    }

    /* Results Dashboard */
    .results-dashboard {
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }

    .results-dashboard::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-green) 0%, var(--accent-gold) 50%, var(--accent-blue) 100%);
    }

    .results-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .results-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .results-timestamp {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: var(--text-muted);
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 1rem;
    }

    .metric-card {
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease forwards;
        opacity: 0;
    }

    .metric-card:nth-child(1) { animation-delay: 0.1s; }
    .metric-card:nth-child(2) { animation-delay: 0.2s; }
    .metric-card:nth-child(3) { animation-delay: 0.3s; }
    .metric-card:nth-child(4) { animation-delay: 0.4s; }
    .metric-card:nth-child(5) { animation-delay: 0.5s; }
    .metric-card:nth-child(6) { animation-delay: 0.6s; }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .metric-card:hover {
        transform: translateY(-2px);
        border-color: var(--accent-gold);
    }

    .metric-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.75rem;
        font-weight: 600;
        line-height: 1.2;
    }

    .metric-value.gold { color: var(--accent-gold); }
    .metric-value.green { color: var(--accent-green); }
    .metric-value.blue { color: var(--accent-blue); }
    .metric-value.red { color: var(--accent-red); }

    .metric-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-top: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .metric-sublabel {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--text-muted);
        margin-top: 0.15rem;
    }

    /* Quality Score Ring */
    .quality-ring {
        width: 80px;
        height: 80px;
        margin: 0 auto 0.5rem;
        position: relative;
    }

    .quality-ring svg {
        transform: rotate(-90deg);
    }

    .quality-ring-bg {
        fill: none;
        stroke: var(--bg-tertiary);
        stroke-width: 6;
    }

    .quality-ring-progress {
        fill: none;
        stroke: var(--accent-gold);
        stroke-width: 6;
        stroke-linecap: round;
        transition: stroke-dashoffset 1s ease;
    }

    .quality-ring-value {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--accent-gold);
    }

    /* Test Results Bar */
    .test-results-bar {
        display: flex;
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        margin: 0.5rem 0;
        background: var(--bg-tertiary);
    }

    .test-results-passed {
        background: var(--accent-green);
        transition: width 0.5s ease;
    }

    .test-results-failed {
        background: var(--accent-red);
        transition: width 0.5s ease;
    }

    .test-results-legend {
        display: flex;
        justify-content: space-between;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
    }

    .legend-passed { color: var(--accent-green); }
    .legend-failed { color: var(--accent-red); }

    /* Collapsible Output */
    .output-toggle {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        margin-top: 1rem;
    }

    .output-toggle summary {
        padding: 0.75rem 1rem;
        cursor: pointer;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: var(--text-secondary);
        list-style: none;
    }

    .output-toggle summary::-webkit-details-marker {
        display: none;
    }

    .output-toggle summary::before {
        content: '> ';
        color: var(--accent-gold);
    }

    .output-toggle[open] summary::before {
        content: 'v ';
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


def get_context_preview(file_path: Path, context_level: str, class_name: str = None):
    """Extract context at specified level for preview."""
    try:
        from class_context_extractor import ClassContextExtractor
        extractor = ClassContextExtractor(file_path, class_name)
        return extractor.extract_context(context_level)
    except Exception as e:
        return f"Error extracting context: {e}"


# Pipeline steps definition
PIPELINE_STEPS = [
    {"id": "context", "name": "Extracting Context", "icon": "1", "patterns": ["extract", "context", "ClassContextExtractor"]},
    {"id": "prompt", "name": "Generating Prompt", "icon": "2", "patterns": ["prompt", "strategy", "Executing"]},
    {"id": "llm", "name": "Calling LLM", "icon": "3", "patterns": ["client", "Initialized", "Claude", "Gemini", "sending"]},
    {"id": "extract_tests", "name": "Extracting Tests", "icon": "4", "patterns": ["extract", "test", "parsing", "Generated"]},
    {"id": "coverage", "name": "Running Coverage", "icon": "5", "patterns": ["coverage", "Coverage", "statement", "branch"]},
    {"id": "mutation", "name": "Mutation Testing", "icon": "6", "patterns": ["mutmut", "mutation", "Mutation", "mutant"]},
    {"id": "metrics", "name": "Computing Metrics", "icon": "7", "patterns": ["quality", "score", "metrics", "completed"]},
]


def detect_current_step(output_lines: list) -> tuple:
    """Detect current pipeline step from output lines.

    Returns:
        tuple: (current_step_index, completed_steps, has_error)
    """
    if not output_lines:
        return 0, set(), False

    completed = set()
    current = 0
    has_error = False

    full_output = "\n".join(output_lines).lower()

    # Check for errors
    if "error" in full_output or "failed" in full_output or "exception" in full_output:
        if "experiment failed" in full_output or "traceback" in full_output:
            has_error = True

    # Detect which steps are completed based on output patterns
    for i, step in enumerate(PIPELINE_STEPS):
        step_found = any(pattern.lower() in full_output for pattern in step["patterns"])
        if step_found:
            current = max(current, i)
            if i < len(PIPELINE_STEPS) - 1:
                # Check if next step has started (meaning this one is complete)
                next_step = PIPELINE_STEPS[i + 1]
                next_found = any(pattern.lower() in full_output for pattern in next_step["patterns"])
                if next_found:
                    completed.add(i)

    # Check for completion markers
    if "experiment completed" in full_output or "results saved" in full_output.lower():
        completed = set(range(len(PIPELINE_STEPS)))
        current = len(PIPELINE_STEPS) - 1

    return current, completed, has_error


def parse_experiment_results(results_dir: str, strategy: str, context: str, model: str) -> dict:
    """Parse experiment results from the most recent run."""
    try:
        base_path = Path(results_dir) / strategy / context / model

        if not base_path.exists():
            return None

        # Find most recent run
        runs = sorted([d for d in base_path.iterdir() if d.is_dir() and d.name.startswith("run_")],
                      key=lambda x: x.name, reverse=True)

        if not runs:
            # Check if results are in base_path (legacy mode)
            run_dir = base_path
        else:
            run_dir = runs[0]

        # Look for analysis_results.json (contains all metrics in summary)
        analysis_file = run_dir / "analysis_results.json"

        if not analysis_file.exists():
            # Fallback to experiment_results.json for basic data
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
                    "total_test_methods": 0,
                    "assertions_count": 0,
                    "run_dir": str(run_dir),
                }
            return None

        with open(analysis_file) as f:
            data = json.load(f)

        # Extract from summary section
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
            "total_test_methods": summary.get("total_test_methods", 0),
            "assertions_count": summary.get("total_assertions", 0),
            "run_dir": str(run_dir),
        }
    except Exception as e:
        return None


def render_pipeline_progress(current_step: int, completed_steps: set, has_error: bool, use_native: bool = True):
    """Render pipeline progress visualization.

    Args:
        current_step: Current step index
        completed_steps: Set of completed step indices
        has_error: Whether an error occurred
        use_native: Use native Streamlit components (for live updates)
    """
    if use_native:
        # Native Streamlit rendering for live updates
        st.markdown("**Pipeline Progress**")

        # Progress bar
        total_steps = len(PIPELINE_STEPS)
        completed_count = len(completed_steps)
        progress = completed_count / total_steps
        st.progress(progress)

        # Steps as columns
        cols = st.columns(len(PIPELINE_STEPS))
        for i, (col, step) in enumerate(zip(cols, PIPELINE_STEPS)):
            with col:
                if i in completed_steps:
                    st.markdown(f"✅")
                    st.caption(step['name'].split()[0])
                elif i == current_step and not has_error:
                    st.markdown(f"🔄")
                    st.caption(step['name'].split()[0])
                elif has_error and i == current_step:
                    st.markdown(f"❌")
                    st.caption(step['name'].split()[0])
                else:
                    st.markdown(f"⏳")
                    st.caption(step['name'].split()[0])

        # Current step status
        if current_step < len(PIPELINE_STEPS):
            current_name = PIPELINE_STEPS[current_step]['name']
            if has_error:
                st.error(f"Error: {current_name}")
            elif current_step in completed_steps:
                st.success(f"Completed: {current_name}")
            else:
                st.info(f"Running: {current_name}...")
    else:
        # HTML rendering for static display (after completion)
        steps_html = ""
        for i, step in enumerate(PIPELINE_STEPS):
            if i in completed_steps:
                status = "completed"
                icon = "✓"
                status_text = "Completed"
            elif i == current_step and not has_error:
                status = "active"
                icon = "●"
                status_text = "In progress..."
            elif has_error and i == current_step:
                status = "error"
                icon = "✗"
                status_text = "Error"
            else:
                status = "pending"
                icon = step["icon"]
                status_text = "Waiting"

            steps_html += f"""
            <div class="pipeline-step {status}">
                <div class="step-icon {status}">{icon}</div>
                <div class="step-content">
                    <div class="step-name">{step['name']}</div>
                    <div class="step-status">{status_text}</div>
                </div>
            </div>
            """

        st.markdown(f"""
        <div class="pipeline-container">
            <div class="pipeline-header">
                <span>Pipeline Progress</span>
            </div>
            <div class="pipeline-steps">
                {steps_html}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_results_dashboard(results: dict, timestamp: str = None):
    """Render results dashboard with metrics using native Streamlit components."""
    if not results:
        return

    stmt_cov = results.get("statement_coverage", 0)
    branch_cov = results.get("branch_coverage", 0)
    mut_score = results.get("mutation_score", 0)
    quality = results.get("quality_score", 0)
    tests_passed = results.get("tests_passed", 0)
    tests_failed = results.get("tests_failed", 0)
    total_tests = results.get("total_tests", 0)
    response_time = results.get("response_time", 0)

    # Header
    st.markdown("---")
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.markdown("### 📊 Experiment Results")
    with header_col2:
        if timestamp:
            st.caption(f"⏰ {timestamp}")

    # Main metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        delta_color = "normal" if stmt_cov >= 80 else "off"
        st.metric(
            label="Statement Coverage",
            value=f"{stmt_cov:.1f}%",
            delta="Good" if stmt_cov >= 80 else ("Fair" if stmt_cov >= 60 else "Low"),
            delta_color=delta_color
        )

    with col2:
        st.metric(
            label="Branch Coverage",
            value=f"{branch_cov:.1f}%"
        )

    with col3:
        delta_color = "normal" if mut_score >= 30 else "off"
        st.metric(
            label="Mutation Score",
            value=f"{mut_score:.1f}%",
            delta="Good" if mut_score >= 40 else ("Fair" if mut_score >= 25 else "Low"),
            delta_color=delta_color
        )

    with col4:
        st.metric(
            label="Quality Score",
            value=f"{quality:.0f}/100"
        )

    # Secondary metrics row
    col5, col6, col7 = st.columns(3)

    with col5:
        st.metric(
            label="Response Time",
            value=f"{response_time:.1f}s"
        )

    with col6:
        st.metric(
            label="Test Methods",
            value=f"{total_tests}"
        )

    with col7:
        if total_tests > 0:
            pass_rate = (tests_passed / total_tests) * 100
            st.metric(
                label="Tests Passed",
                value=f"{tests_passed}/{total_tests}",
                delta=f"{pass_rate:.0f}%",
                delta_color="normal" if tests_failed == 0 else "off"
            )
        else:
            st.metric(label="Tests Passed", value="N/A")

    # Test results progress bar
    if total_tests > 0:
        st.progress(tests_passed / total_tests)
        pass_col, fail_col = st.columns(2)
        with pass_col:
            st.caption(f"✅ {tests_passed} passed")
        with fail_col:
            st.caption(f"❌ {tests_failed} failed")

    st.markdown("---")


def run_experiment(source_file: str, model: str, strategy: str, context: str,
                   class_name: str = None, run_id: int = None, results_dir: str = None):
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
    if results_dir:
        cmd.extend(["--results-dir", results_dir])

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
    if "experiment_metrics" not in st.session_state:
        st.session_state.experiment_metrics = None
    if "show_output" not in st.session_state:
        st.session_state.show_output = False

    render_header()

    with st.sidebar:
        st.markdown('<span class="section-label">Configuration</span>', unsafe_allow_html=True)

        mode = st.radio(
            "Mode",
            ["Universal (Any Class)", "Legacy (OrderCalculator)"]
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
                    st.success(f"Class '{class_info.name}' detected successfully")
                    render_class_info(class_info)
                else:
                    st.warning("Multiple classes found or detection failed")
                    class_name = st.text_input(
                        "Class name (specify which class to test)",
                        placeholder="ClassName"
                    )
                    if class_name:
                        class_info = get_class_info(Path(source_file), class_name)
                        if class_info:
                            st.success(f"Class '{class_info.name}' loaded successfully")
                            render_class_info(class_info)
                        else:
                            st.error(f"Could not load class '{class_name}'")
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

        # Context preview
        if class_info:
            preview_source = source_file if mode == "Universal (Any Class)" else str(Path(__file__).parent / "order_calculator.py")
            if preview_source and Path(preview_source).exists():
                with st.expander("Preview extracted context", expanded=False):
                    context_preview = get_context_preview(
                        Path(preview_source),
                        context,
                        class_name
                    )
                    if context_preview and not context_preview.startswith("Error"):
                        st.success(f"Context extracted successfully ({len(context_preview)} characters)")
                        st.code(context_preview, language="python")
                    else:
                        st.error(context_preview)

        st.divider()

        st.markdown('<span class="section-label">Run Options</span>',
                   unsafe_allow_html=True)
        run_id = st.number_input("Run ID (auto if 0)", min_value=0, value=0)

        results_dir = st.text_input(
            "Results directory",
            value="cli_results"
        )

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
            elif st.session_state.last_result and st.session_state.last_result.get("success"):
                render_status("ready")
            elif st.session_state.last_result:
                render_status("error")
            else:
                render_status("ready")

        with status_col2:
            if st.session_state.experiment_running:
                st.caption("Experiment in progress...")
            elif st.session_state.last_result:
                st.caption(f"Last run: {st.session_state.last_result.get('timestamp', 'N/A')}")
            else:
                st.caption("Configure and run an experiment")

        # Pipeline progress and output area
        pipeline_placeholder = st.empty()
        output_placeholder = st.empty()

        if st.session_state.experiment_running:
            process = run_experiment(
                source_file if mode == "Universal (Any Class)" else None,
                selected_model,
                strategy,
                context,
                class_name,
                run_id if run_id > 0 else None,
                results_dir if results_dir != "cli_results" else None
            )

            output_lines = []
            for line in process.stdout:
                output_lines.append(line.strip())

                # Update pipeline progress (native components)
                current_step, completed_steps, has_error = detect_current_step(output_lines)
                with pipeline_placeholder.container():
                    render_pipeline_progress(current_step, completed_steps, has_error, use_native=True)

                # Update console output
                output_placeholder.code("\n".join(output_lines[-30:]), language="")

            process.wait()
            success = process.returncode == 0

            # Parse experiment results
            actual_results_dir = results_dir if results_dir else "cli_results"
            experiment_metrics = parse_experiment_results(actual_results_dir, strategy, context, selected_model)

            st.session_state.experiment_running = False
            st.session_state.experiment_output = output_lines
            st.session_state.experiment_metrics = experiment_metrics
            st.session_state.last_result = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "model": selected_model,
                "strategy": strategy,
                "context": context,
                "success": success,
                "results_dir": actual_results_dir
            }
            st.rerun()
        else:
            # Show completed pipeline (use native for consistency)
            if st.session_state.experiment_output:
                current_step, completed_steps, has_error = detect_current_step(st.session_state.experiment_output)

                # If experiment completed successfully, mark all as completed
                if st.session_state.last_result and st.session_state.last_result.get("success"):
                    completed_steps = set(range(len(PIPELINE_STEPS)))
                    has_error = False

                render_pipeline_progress(len(PIPELINE_STEPS) - 1, completed_steps, has_error, use_native=True)

            # Show results dashboard if available
            if st.session_state.experiment_metrics:
                timestamp = st.session_state.last_result.get("timestamp") if st.session_state.last_result else None
                render_results_dashboard(st.session_state.experiment_metrics, timestamp)

            # Collapsible console output
            if st.session_state.experiment_output:
                with st.expander("Console Output", expanded=False):
                    st.code("\n".join(st.session_state.experiment_output[-100:]), language="")
            else:
                st.info("No experiments run yet. Configure parameters and click 'Run Experiment'.")

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
            st.markdown("**Last Run**")

            result = st.session_state.last_result
            metrics = st.session_state.experiment_metrics

            # Time and status
            st.caption(f"⏰ {result.get('timestamp', 'N/A')}")
            if result.get('success'):
                st.success("✅ Success")
            else:
                st.error("❌ Failed")

            # Metrics if available
            if metrics and result.get('success'):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Coverage", f"{metrics.get('statement_coverage', 0):.1f}%")
                with col_b:
                    st.metric("Mutation", f"{metrics.get('mutation_score', 0):.1f}%")
                st.metric("Quality", f"{metrics.get('quality_score', 0):.0f}/100")

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
