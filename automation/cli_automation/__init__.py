"""
CLI-based LLM automation package

This package provides CLI-based clients for various LLM tools:
- OpenAI Codex CLI (CodexCLIClient)
- Claude Code CLI (ClaudeCodeClient)
- Google Gemini CLI (GeminiCLIClient)

All clients inherit from BaseCLIClient for consistent interface.

Usage:
    from cli_automation import CodexCLIClient, ClaudeCodeClient

    # Claude Code
    with ClaudeCodeClient(model="claude-sonnet-4.5") as client:
        response = client.send_prompt("Write tests...")
"""

from .base_cli_client import BaseCLIClient
from .codex_client import CodexCLIClient
from .claude_code_client import ClaudeCodeClient
from .copilot_cli_client import CopilotCLIClient
from .gemini_cli_client import GeminiCLIClient

__all__ = [
    'BaseCLIClient',
    'CodexCLIClient',
    'ClaudeCodeClient',
    'CopilotCLIClient',
    'GeminiCLIClient'
]

__version__ = '1.0.0'
