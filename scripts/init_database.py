#!/usr/bin/env python3
"""
Initialize Neon database schema
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.connection import get_db_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_database():
    """Initialize database schema"""
    try:
        logger.info("🚀 Initializing Claude Education Platform database...")
        
        # Get database manager and connect
        db = await get_db_manager()
        
        logger.info("✅ Database connection established")
        logger.info("✅ All tables created successfully")
        
        # Test basic operations
        test_id = await db.add_student_progress(
            student_id="test_student",
            topic="database_initialization",
            completion_score=100.0,
            time_spent=5
        )
        
        logger.info(f"✅ Test record created with ID: {test_id}")
        
        # Test research source
        research_id = await db.save_research_source(
            topic="python_basics",
            age_group="10-16",
            language="spanish",
            content_data={
                "test": "data",
                "tutorials": ["example tutorial"],
                "examples": ["example code"]
            },
            tutorial_count=1,
            example_count=1,
            estimated_time="30 minutes"
        )
        
        logger.info(f"✅ Test research source created with ID: {research_id}")
        
        # Cleanup test data
        await db.execute("DELETE FROM student_progress WHERE student_id = 'test_student'")
        await db.execute("DELETE FROM research_sources WHERE id = $1", research_id)
        
        logger.info("✅ Test data cleaned up")
        logger.info("🎉 Database initialization complete!")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    finally:
        if 'db' in locals():
            await db.disconnect()

if __name__ == "__main__":
    asyncio.run(init_database())