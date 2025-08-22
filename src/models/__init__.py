"""
AI Model Management System for Claude Education Platform
Supports multiple model providers including DeepSeek, OpenAI, and Hugging Face
"""

from .model_manager import ModelManager
from .deepseek_client import DeepSeekClient
from .model_config import ModelConfig

__all__ = ['ModelManager', 'DeepSeekClient', 'ModelConfig']