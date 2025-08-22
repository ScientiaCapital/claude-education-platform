"""
Legacy database module - use src.database.connection instead
This file is kept for backwards compatibility
"""

# Import the new database manager
from src.database.connection import get_db_manager

# Legacy compatibility
class DatabaseManager:
    """Legacy wrapper for backwards compatibility"""
    
    def __init__(self):
        self._db_manager = None
    
    async def _get_db(self):
        if self._db_manager is None:
            self._db_manager = await get_db_manager()
        return self._db_manager
    
    async def add_student_progress(self, student_id: str, topic: str, completion_score: float, time_spent: int):
        """Record student progress"""
        db = await self._get_db()
        return await db.add_student_progress(student_id, topic, completion_score, time_spent)
    
    async def add_lesson_content(self, title: str, content: str, difficulty_level: str, topic_category: str):
        """Add new lesson content"""
        db = await self._get_db()
        return await db.add_lesson_content(title, content, difficulty_level, topic_category)
    
    async def record_interaction(self, student_id: str, question: str, answer: str, tutor_type: str, satisfaction_rating: int = None):
        """Record student-tutor interaction"""
        db = await self._get_db()
        return await db.record_interaction(student_id, question, answer, tutor_type, satisfaction_rating)
    
    async def get_student_progress(self, student_id: str):
        """Get all progress for a student"""
        db = await self._get_db()
        return await db.get_student_progress(student_id)
    
    async def get_lessons_by_category(self, topic_category: str, difficulty_level: str = None):
        """Get lessons by category and optional difficulty"""
        db = await self._get_db()
        return await db.get_lessons_by_category(topic_category, difficulty_level)

# Initialize database manager
db_manager = DatabaseManager()