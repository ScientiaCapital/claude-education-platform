"""
AI Model Management System for Claude Education Platform
Supports multiple model providers including DeepSeek, OpenAI, and Hugging Face
"""

from .deepseek_client import DeepSeekClient

__all__ = ['DeepSeekClient']