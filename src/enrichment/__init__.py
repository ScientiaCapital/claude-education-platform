"""
Educational content enrichment pipeline for Claude Education Platform

This module provides intelligent content discovery and enrichment
specifically designed for educational use cases.
"""

from .educational_enricher import EducationalEnricher
from .curriculum_monitor import CurriculumMonitor

__all__ = ['EducationalEnricher', 'CurriculumMonitor']