"""
Async database wrapper for the education platform
Provides a consistent async interface for database operations
"""

import asyncio
from typing import Optional, List, Dict, Any
from src.database.connection import get_db_manager
from src.database.models import StudentProgress

class AsyncDatabaseManager:
    """Async database manager with proper connection handling"""
    
    def __init__(self):
        self._db_manager = None
        self._initialized = False
    
    async def _ensure_connected(self):
        """Ensure database is connected before operations"""
        if self._db_manager is None:
            self._db_manager = await get_db_manager()
            self._initialized = True
        return self._db_manager
    
    async def create_tables(self):
        """Create all database tables"""
        db = await self._ensure_connected()
        await db.create_tables()
    
    async def add_student_progress(
        self, 
        student_id: str, 
        topic: str, 
        completion_score: float, 
        time_spent: int
    ) -> StudentProgress:
        """Record student progress"""
        db = await self._ensure_connected()
        progress_id = await db.add_student_progress(
            student_id, topic, completion_score, time_spent
        )
        return StudentProgress(
            id=progress_id,
            student_id=student_id,
            topic=topic,
            completion_score=completion_score,
            time_spent=time_spent
        )
    
    async def add_lesson_content(
        self, 
        title: str, 
        content: str, 
        difficulty_level: str, 
        topic_category: str
    ) -> int:
        """Add new lesson content"""
        db = await self._ensure_connected()
        return await db.add_lesson_content(
            title, content, difficulty_level, topic_category
        )
    
    async def record_interaction(
        self, 
        student_id: str, 
        question: str, 
        answer: str, 
        tutor_type: str, 
        satisfaction_rating: Optional[int] = None
    ) -> int:
        """Record student-tutor interaction"""
        db = await self._ensure_connected()
        return await db.record_interaction(
            student_id, question, answer, tutor_type, satisfaction_rating
        )
    
    async def get_student_progress(self, student_id: str) -> List[StudentProgress]:
        """Get all progress for a student"""
        db = await self._ensure_connected()
        results = await db.get_student_progress(student_id)
        return [
            StudentProgress(
                id=r['id'],
                student_id=r['student_id'],
                topic=r['topic'],
                completion_score=r['completion_score'],
                time_spent=r['time_spent'],
                created_at=r['created_at']
            )
            for r in results
        ]
    
    async def get_lessons_by_category(
        self, 
        topic_category: str, 
        difficulty_level: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get lessons by category and optional difficulty"""
        db = await self._ensure_connected()
        return await db.get_lessons_by_category(topic_category, difficulty_level)

# Initialize global database manager instance
db_manager = AsyncDatabaseManager()