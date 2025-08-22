"""
Database module for Claude Education Platform
"""

from .connection import DatabaseManager
from .models import (
    StudentProgress, 
    LessonContent, 
    StudentInteraction,
    ResearchSource,
    CurriculumUpdate,
    StudentResearch,
    EducationalLead,
    CacheEntry
)

__all__ = [
    'DatabaseManager',
    'StudentProgress',
    'LessonContent', 
    'StudentInteraction',
    'ResearchSource',
    'CurriculumUpdate',
    'StudentResearch',
    'EducationalLead',
    'CacheEntry'
]