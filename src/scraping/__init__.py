"""
Advanced web scraping module for Claude Education Platform

This module provides intelligent web scraping capabilities specifically
designed for educational content discovery and research.
"""

from .core import EducationalScraper
from .cache import SmartCache
from .rate_limiter import EducationalRateLimiter

__all__ = ['EducationalScraper', 'SmartCache', 'EducationalRateLimiter']