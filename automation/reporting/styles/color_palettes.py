"""
Color palettes for thesis figures.

Provides consistent, colorblind-friendly color schemes for all charts.
"""

# Model colors - distinct, colorblind-friendly
MODEL_COLORS = {
    'claude-code-opus-4.5': '#2E86AB',      # Blue
    'claude-code-sonnet-4.5': '#A23B72',    # Magenta
    'claude-code-opus-4.1': '#F18F01',      # Orange
    'gemini-3-pro': '#C73E1D',              # Red
    'gemini-3-flash': '#3B1F2B',            # Dark purple
    'gemini-2.5-pro': '#95C623',            # Green
    'gemini-2.5-flash': '#7B2D26',          # Brown
}

# Strategy colors
STRATEGY_COLORS = {
    'simple_prompting': '#2E86AB',          # Blue
    'chain_of_thought_prompting': '#C73E1D' # Red
}

# Context level colors
CONTEXT_COLORS = {
    'interface': '#2E86AB',                 # Blue
    'interface_docstring': '#F18F01',       # Orange
    'full_context': '#95C623'               # Green
}

# Qualitative palette (8 colors)
QUALITATIVE_PALETTE = [
    '#2E86AB',  # Blue
    '#A23B72',  # Magenta
    '#F18F01',  # Orange
    '#C73E1D',  # Red
    '#95C623',  # Green
    '#7B2D26',  # Brown
    '#3B1F2B',  # Dark purple
    '#6B4C9A',  # Purple
]

# Sequential palette for heatmaps (green to red via yellow)
DIVERGING_PALETTE = 'RdYlGn'

# Monochrome palette
MONO_PALETTE = [
    '#1a1a1a',  # Dark
    '#4d4d4d',  # Medium dark
    '#808080',  # Medium
    '#b3b3b3',  # Medium light
    '#e6e6e6',  # Light
]


def get_model_color(model: str, default: str = '#888888') -> str:
    """Get color for a model, with fallback."""
    return MODEL_COLORS.get(model, default)


def get_strategy_color(strategy: str, default: str = '#888888') -> str:
    """Get color for a strategy, with fallback."""
    return STRATEGY_COLORS.get(strategy, default)


def get_context_color(context: str, default: str = '#888888') -> str:
    """Get color for a context level, with fallback."""
    return CONTEXT_COLORS.get(context, default)
