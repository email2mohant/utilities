"""
LangChain Ollama OpenAPI Agent Module

This module provides a FastAPI service for interacting with OpenAPI specifications
using LangChain and Ollama's LLM models.
"""

from .api import create_app, run_server
from .agent import create_agent, AgentManager

__version__ = "0.1.0"
__all__ = ["create_app", "run_server", "create_agent", "AgentManager"]