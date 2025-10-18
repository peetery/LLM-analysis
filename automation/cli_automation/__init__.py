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
from .claude_code_client import ClaudeCodeClient

__all__ = [
    'BaseCLIClient',
    'ClaudeCodeClient',
]

__version__ = '1.0.0'
