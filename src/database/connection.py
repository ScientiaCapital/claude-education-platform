"""
Neon PostgreSQL database connection and management
"""

import asyncio
import asyncpg
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from config.settings import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Async database manager for Neon PostgreSQL
    """
    
    def __init__(self):
        self.pool = None
        self._connection_url = settings.database_url
    
    async def connect(self):
        """Initialize connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                self._connection_url,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
            logger.info("📊 Connected to Neon PostgreSQL database")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    async def disconnect(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("📊 Disconnected from database")
    
    async def execute(self, query: str, *args) -> str:
        """Execute a query and return result"""
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
    
    async def fetch(self, query: str, *args) -> List[Dict]:
        """Fetch multiple rows"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]
    
    async def fetchrow(self, query: str, *args) -> Optional[Dict]:
        """Fetch single row"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None
    
    async def fetchval(self, query: str, *args) -> Any:
        """Fetch single value"""
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)
    
    async def create_tables(self):
        """Create all required tables"""
        
        # Original tables from existing schema
        await self._create_original_tables()
        
        # New tables for educational research
        await self._create_research_tables()
        
        # Cache tables
        await self._create_cache_tables()
        
        logger.info("✅ All database tables created successfully")
    
    async def _create_original_tables(self):
        """Create original student/lesson tables"""
        
        # Student progress table
        await self.execute("""
            CREATE TABLE IF NOT EXISTS student_progress (
                id SERIAL PRIMARY KEY,
                student_id VARCHAR(100) NOT NULL,
                topic VARCHAR(200) NOT NULL,
                completion_score FLOAT NOT NULL,
                time_spent INTEGER NOT NULL, -- minutes
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_student_progress_student_id ON student_progress(student_id)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_student_progress_topic ON student_progress(topic)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_student_progress_created_at ON student_progress(created_at)
        """)
        
        # Lesson content table
        await self.execute("""
            CREATE TABLE IF NOT EXISTS lesson_content (
                id SERIAL PRIMARY KEY,
                title VARCHAR(500) NOT NULL,
                content TEXT NOT NULL,
                difficulty_level VARCHAR(50) NOT NULL, -- beginner, intermediate, advanced
                topic_category VARCHAR(100) NOT NULL, -- chatbot, ai_training, programming
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_lesson_content_difficulty ON lesson_content(difficulty_level)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_lesson_content_category ON lesson_content(topic_category)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_lesson_content_created_at ON lesson_content(created_at)
        """)
        
        # Student interactions table
        await self.execute("""
            CREATE TABLE IF NOT EXISTS student_interactions (
                id SERIAL PRIMARY KEY,
                student_id VARCHAR(100) NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                tutor_type VARCHAR(100) NOT NULL,
                satisfaction_rating INTEGER, -- 1-5
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_student_interactions_student_id ON student_interactions(student_id)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_student_interactions_tutor_type ON student_interactions(tutor_type)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_student_interactions_created_at ON student_interactions(created_at)
        """)
    
    async def _create_research_tables(self):
        """Create tables for educational research functionality"""
        
        # Research sources table
        await self.execute("""
            CREATE TABLE IF NOT EXISTS research_sources (
                id SERIAL PRIMARY KEY,
                topic VARCHAR(200) NOT NULL,
                age_group VARCHAR(20) NOT NULL, -- 10-16, 14-18
                language VARCHAR(20) NOT NULL, -- spanish, english
                content_data JSONB NOT NULL, -- Full enriched content
                tutorial_count INTEGER DEFAULT 0,
                example_count INTEGER DEFAULT 0,
                estimated_time VARCHAR(50),
                relevance_score FLOAT DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_research_sources_topic ON research_sources(topic)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_research_sources_age_group ON research_sources(age_group)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_research_sources_language ON research_sources(language)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_research_sources_relevance ON research_sources(relevance_score)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_research_sources_created_at ON research_sources(created_at)
        """)
        
        # Curriculum updates tracking
        await self.execute("""
            CREATE TABLE IF NOT EXISTS curriculum_updates (
                id SERIAL PRIMARY KEY,
                topic VARCHAR(200) NOT NULL,
                update_type VARCHAR(50) NOT NULL, -- enrichment, correction, expansion
                source_url TEXT,
                new_content JSONB,
                confidence_score FLOAT DEFAULT 0.0,
                applied BOOLEAN DEFAULT FALSE,
                reviewed_by VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                applied_at TIMESTAMP
            )
        """)
        
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_curriculum_updates_topic ON curriculum_updates(topic)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_curriculum_updates_type ON curriculum_updates(update_type)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_curriculum_updates_applied ON curriculum_updates(applied)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_curriculum_updates_created_at ON curriculum_updates(created_at)
        """)
        
        # Student research tracking
        await self.execute("""
            CREATE TABLE IF NOT EXISTS student_research (
                id SERIAL PRIMARY KEY,
                student_id VARCHAR(100) NOT NULL,
                research_topic VARCHAR(200) NOT NULL,
                search_queries TEXT[], -- Array of search queries used
                sources_found INTEGER DEFAULT 0,
                time_spent INTEGER DEFAULT 0, -- minutes
                difficulty_requested VARCHAR(20),
                language_preference VARCHAR(20),
                results_data JSONB, -- Research results
                satisfaction_rating INTEGER, -- 1-5
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)
        
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_student_research_student_id ON student_research(student_id)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_student_research_topic ON student_research(research_topic)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_student_research_difficulty ON student_research(difficulty_requested)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_student_research_created_at ON student_research(created_at)
        """)
        
        # Educational leads (potential learning opportunities)
        await self.execute("""
            CREATE TABLE IF NOT EXISTS educational_leads (
                id SERIAL PRIMARY KEY,
                source_type VARCHAR(50) NOT NULL, -- firecrawl, tavily, exa
                url TEXT NOT NULL UNIQUE,
                title VARCHAR(500),
                description TEXT,
                topic_relevance JSONB, -- Topics and relevance scores
                content_type VARCHAR(50), -- tutorial, documentation, course, example
                difficulty_estimate VARCHAR(20),
                language VARCHAR(20),
                quality_score FLOAT DEFAULT 0.0,
                processing_status VARCHAR(50) DEFAULT 'pending', -- pending, processed, enriched, archived
                last_scraped TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_educational_leads_source_type ON educational_leads(source_type)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_educational_leads_content_type ON educational_leads(content_type)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_educational_leads_difficulty ON educational_leads(difficulty_estimate)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_educational_leads_quality ON educational_leads(quality_score)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_educational_leads_status ON educational_leads(processing_status)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_educational_leads_created_at ON educational_leads(created_at)
        """)
    
    async def _create_cache_tables(self):
        """Create tables for intelligent caching"""
        
        await self.execute("""
            CREATE TABLE IF NOT EXISTS cache_entries (
                id SERIAL PRIMARY KEY,
                cache_key VARCHAR(64) NOT NULL UNIQUE,
                cache_type VARCHAR(50) NOT NULL,
                url TEXT,
                data JSONB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                hit_count INTEGER DEFAULT 0,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_cache_entries_type ON cache_entries(cache_type)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_cache_entries_expires ON cache_entries(expires_at)
        """)
        await self.execute("""
            CREATE INDEX IF NOT EXISTS idx_cache_entries_accessed ON cache_entries(last_accessed)
        """)
    
    # Cache management methods
    async def set_cache(
        self, 
        cache_key: str, 
        cache_type: str, 
        data: Dict, 
        expires_hours: int = 24,
        url: str = None
    ):
        """Set cache entry"""
        expires_at = datetime.now() + timedelta(hours=expires_hours)
        
        await self.execute("""
            INSERT INTO cache_entries (cache_key, cache_type, url, data, expires_at)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (cache_key) 
            DO UPDATE SET 
                data = EXCLUDED.data,
                expires_at = EXCLUDED.expires_at,
                last_accessed = CURRENT_TIMESTAMP,
                hit_count = cache_entries.hit_count + 1
        """, cache_key, cache_type, url, json.dumps(data), expires_at)
    
    async def get_cache(self, cache_key: str) -> Optional[Dict]:
        """Get cache entry if not expired"""
        result = await self.fetchrow("""
            SELECT data FROM cache_entries 
            WHERE cache_key = $1 AND expires_at > CURRENT_TIMESTAMP
        """, cache_key)
        
        if result:
            # Update hit count and last accessed
            await self.execute("""
                UPDATE cache_entries 
                SET hit_count = hit_count + 1, last_accessed = CURRENT_TIMESTAMP
                WHERE cache_key = $1
            """, cache_key)
            
            return json.loads(result['data'])
        
        return None
    
    async def cleanup_expired_cache(self) -> int:
        """Clean up expired cache entries"""
        result = await self.execute("""
            DELETE FROM cache_entries WHERE expires_at < CURRENT_TIMESTAMP
        """)
        
        # Extract count from result string like "DELETE 5"
        count = int(result.split()[-1]) if result.split()[-1].isdigit() else 0
        return count
    
    # Student progress methods
    async def add_student_progress(
        self, 
        student_id: str, 
        topic: str, 
        completion_score: float, 
        time_spent: int
    ) -> int:
        """Record student progress"""
        result = await self.fetchval("""
            INSERT INTO student_progress (student_id, topic, completion_score, time_spent)
            VALUES ($1, $2, $3, $4)
            RETURNING id
        """, student_id, topic, completion_score, time_spent)
        
        return result
    
    async def get_student_progress(self, student_id: str) -> List[Dict]:
        """Get all progress for a student"""
        return await self.fetch("""
            SELECT * FROM student_progress 
            WHERE student_id = $1 
            ORDER BY created_at DESC
        """, student_id)
    
    # Lesson content methods
    async def add_lesson_content(
        self, 
        title: str, 
        content: str, 
        difficulty_level: str, 
        topic_category: str
    ) -> int:
        """Add new lesson content"""
        result = await self.fetchval("""
            INSERT INTO lesson_content (title, content, difficulty_level, topic_category)
            VALUES ($1, $2, $3, $4)
            RETURNING id
        """, title, content, difficulty_level, topic_category)
        
        return result
    
    async def get_lessons_by_category(
        self, 
        topic_category: str, 
        difficulty_level: str = None
    ) -> List[Dict]:
        """Get lessons by category and optional difficulty"""
        if difficulty_level:
            return await self.fetch("""
                SELECT * FROM lesson_content 
                WHERE topic_category = $1 AND difficulty_level = $2
                ORDER BY created_at DESC
            """, topic_category, difficulty_level)
        else:
            return await self.fetch("""
                SELECT * FROM lesson_content 
                WHERE topic_category = $1
                ORDER BY created_at DESC
            """, topic_category)
    
    # Student interaction methods
    async def record_interaction(
        self, 
        student_id: str, 
        question: str, 
        answer: str, 
        tutor_type: str, 
        satisfaction_rating: int = None
    ) -> int:
        """Record student-tutor interaction"""
        result = await self.fetchval("""
            INSERT INTO student_interactions 
            (student_id, question, answer, tutor_type, satisfaction_rating)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
        """, student_id, question, answer, tutor_type, satisfaction_rating)
        
        return result
    
    # Research source methods
    async def save_research_source(
        self,
        topic: str,
        age_group: str,
        language: str,
        content_data: Dict,
        tutorial_count: int = 0,
        example_count: int = 0,
        estimated_time: str = None,
        relevance_score: float = 0.0
    ) -> int:
        """Save enriched research content"""
        result = await self.fetchval("""
            INSERT INTO research_sources 
            (topic, age_group, language, content_data, tutorial_count, 
             example_count, estimated_time, relevance_score)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id
        """, topic, age_group, language, json.dumps(content_data), 
        tutorial_count, example_count, estimated_time, relevance_score)
        
        return result
    
    async def get_research_sources(
        self,
        topic: str = None,
        age_group: str = None,
        language: str = None,
        min_relevance: float = 0.0
    ) -> List[Dict]:
        """Get research sources with optional filters"""
        conditions = ["relevance_score >= $1"]
        params = [min_relevance]
        param_count = 1
        
        if topic:
            param_count += 1
            conditions.append(f"topic ILIKE ${param_count}")
            params.append(f"%{topic}%")
        
        if age_group:
            param_count += 1
            conditions.append(f"age_group = ${param_count}")
            params.append(age_group)
        
        if language:
            param_count += 1
            conditions.append(f"language = ${param_count}")
            params.append(language)
        
        query = f"""
            SELECT * FROM research_sources 
            WHERE {' AND '.join(conditions)}
            ORDER BY relevance_score DESC, created_at DESC
        """
        
        return await self.fetch(query, *params)

# Global database manager instance
db_manager = None

async def get_db_manager() -> DatabaseManager:
    """Get or create database manager instance"""
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
        await db_manager.connect()
        await db_manager.create_tables()
    return db_manager