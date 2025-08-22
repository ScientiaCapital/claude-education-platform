from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config.settings import settings

Base = declarative_base()

class StudentProgress(Base):
    __tablename__ = "student_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True)
    topic = Column(String)
    completion_score = Column(Float)
    time_spent = Column(Integer)  # minutes
    created_at = Column(DateTime, default=datetime.utcnow)

class LessonContent(Base):
    __tablename__ = "lesson_content"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    difficulty_level = Column(String)  # beginner, intermediate, advanced
    topic_category = Column(String)  # chatbot, ai_training, programming
    created_at = Column(DateTime, default=datetime.utcnow)

class StudentInteraction(Base):
    __tablename__ = "student_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True)
    question = Column(Text)
    answer = Column(Text)
    tutor_type = Column(String)
    satisfaction_rating = Column(Integer)  # 1-5
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(settings.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Create all tables in the database"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_db(self):
        """Get database session"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def add_student_progress(self, student_id: str, topic: str, completion_score: float, time_spent: int):
        """Record student progress"""
        db = next(self.get_db())
        progress = StudentProgress(
            student_id=student_id,
            topic=topic,
            completion_score=completion_score,
            time_spent=time_spent
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
        return progress
    
    def add_lesson_content(self, title: str, content: str, difficulty_level: str, topic_category: str):
        """Add new lesson content"""
        db = next(self.get_db())
        lesson = LessonContent(
            title=title,
            content=content,
            difficulty_level=difficulty_level,
            topic_category=topic_category
        )
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson
    
    def record_interaction(self, student_id: str, question: str, answer: str, tutor_type: str, satisfaction_rating: int = None):
        """Record student-tutor interaction"""
        db = next(self.get_db())
        interaction = StudentInteraction(
            student_id=student_id,
            question=question,
            answer=answer,
            tutor_type=tutor_type,
            satisfaction_rating=satisfaction_rating
        )
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
        return interaction
    
    def get_student_progress(self, student_id: str):
        """Get all progress for a student"""
        db = next(self.get_db())
        return db.query(StudentProgress).filter(StudentProgress.student_id == student_id).all()
    
    def get_lessons_by_category(self, topic_category: str, difficulty_level: str = None):
        """Get lessons by category and optional difficulty"""
        db = next(self.get_db())
        query = db.query(LessonContent).filter(LessonContent.topic_category == topic_category)
        if difficulty_level:
            query = query.filter(LessonContent.difficulty_level == difficulty_level)
        return query.all()

# Initialize database manager
db_manager = DatabaseManager()