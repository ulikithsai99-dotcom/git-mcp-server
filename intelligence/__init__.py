"""
Intelligence package.

Contains all AI-related components used by the
Software Engineer workflow.
"""

# Base LLM interface
from .llm import LLMProvider

# LLM implementations
from .mock_provider import MockProvider

# Data models
from .models import (
    AIMessage,
    AnalysisRequest,
    AnalysisResponse,
)

# Core intelligence components
from .analyzer import Analyzer
from .parser import ResponseParser
from .repair_engine import RepairEngine

# Prompt library
from .prompts import PromptLibrary


__all__ = [
    # LLM
    "LLMProvider",
    "MockProvider",

    # Models
    "AIMessage",
    "AnalysisRequest",
    "AnalysisResponse",

    # Intelligence
    "Analyzer",
    "ResponseParser",
    "RepairEngine",

    # Prompts
    "PromptLibrary",
]