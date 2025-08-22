"""
Database models for Claude Education Platform
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

@dataclass
class StudentProgress:
    """Student progress model"""
    id: Optional[int] = None
    student_id: str = ""
    topic: str = ""
    completion_score: float = 0.0
    time_spent: int = 0  # minutes
    created_at: Optional[datetime] = None

@dataclass
class LessonContent:
    """Lesson content model"""
    id: Optional[int] = None
    title: str = ""
    content: str = ""
    difficulty_level: str = ""  # beginner, intermediate, advanced
    topic_category: str = ""  # chatbot, ai_training, programming
    created_at: Optional[datetime] = None

@dataclass
class StudentInteraction:
    """Student interaction model"""
    id: Optional[int] = None
    student_id: str = ""
    question: str = ""
    answer: str = ""
    tutor_type: str = ""
    satisfaction_rating: Optional[int] = None  # 1-5
    created_at: Optional[datetime] = None

@dataclass
class ResearchSource:
    """Research source model for educational content"""
    id: Optional[int] = None
    topic: str = ""
    age_group: str = ""  # 10-16, 14-18
    language: str = ""  # spanish, english
    content_data: Dict[str, Any] = None
    tutorial_count: int = 0
    example_count: int = 0
    estimated_time: Optional[str] = None
    relevance_score: float = 0.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class CurriculumUpdate:
    """Curriculum update tracking model"""
    id: Optional[int] = None
    topic: str = ""
    update_type: str = ""  # enrichment, correction, expansion
    source_url: Optional[str] = None
    new_content: Optional[Dict[str, Any]] = None
    confidence_score: float = 0.0
    applied: bool = False
    reviewed_by: Optional[str] = None
    created_at: Optional[datetime] = None
    applied_at: Optional[datetime] = None

@dataclass
class StudentResearch:
    """Student research tracking model"""
    id: Optional[int] = None
    student_id: str = ""
    research_topic: str = ""
    search_queries: List[str] = None
    sources_found: int = 0
    time_spent: int = 0  # minutes
    difficulty_requested: Optional[str] = None
    language_preference: Optional[str] = None
    results_data: Optional[Dict[str, Any]] = None
    satisfaction_rating: Optional[int] = None  # 1-5
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

@dataclass
class EducationalLead:
    """Educational lead model for potential learning opportunities"""
    id: Optional[int] = None
    source_type: str = ""  # firecrawl, tavily, exa
    url: str = ""
    title: Optional[str] = None
    description: Optional[str] = None
    topic_relevance: Optional[Dict[str, Any]] = None
    content_type: Optional[str] = None  # tutorial, documentation, course, example
    difficulty_estimate: Optional[str] = None
    language: Optional[str] = None
    quality_score: float = 0.0
    processing_status: str = "pending"  # pending, processed, enriched, archived
    last_scraped: Optional[datetime] = None
    created_at: Optional[datetime] = None

@dataclass
class CacheEntry:
    """Cache entry model"""
    id: Optional[int] = None
    cache_key: str = ""
    cache_type: str = ""
    url: Optional[str] = None
    data: Dict[str, Any] = None
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    hit_count: int = 0
    last_accessed: Optional[datetime] = None