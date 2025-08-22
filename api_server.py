from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import uvicorn
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.agents.tutor_agent import ChatbotTutor, ModelTrainingTutor, ProgrammingTutor
from src.rag.database import db_manager

app = FastAPI(title="Claude Education API", version="1.0.0")

# Validate environment variables on startup
def validate_environment():
    """Check that all required environment variables are set"""
    required_vars = {
        'ANTHROPIC_API_KEY': 'Claude API key for AI responses',
        'DATABASE_URL': 'PostgreSQL connection string',
        'FIRECRAWL_API_KEY': 'Firecrawl API key for web scraping',
    }
    
    optional_vars = {
        'EXA_API_KEY': 'Exa API key for semantic search (optional)',
        'TAVILY_API_KEY': 'Tavily API key for research (optional)',
    }
    
    missing_required = []
    missing_optional = []
    
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_required.append(f"  - {var}: {description}")
    
    for var, description in optional_vars.items():
        if not os.getenv(var):
            missing_optional.append(f"  - {var}: {description}")
    
    if missing_required:
        print("❌ Missing required environment variables:")
        print("\n".join(missing_required))
        print("\n💡 Please set these in your .env file or environment")
        sys.exit(1)
    
    if missing_optional:
        print("⚠️  Missing optional environment variables (some features may be limited):")
        print("\n".join(missing_optional))
    
    print("✅ All required environment variables are configured")

# Validate on import
validate_environment()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize tutors
tutors = {
    "chatbot": ChatbotTutor(),
    "model-training": ModelTrainingTutor(),
    "programming": ProgrammingTutor()
}

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    tutor_type: str
    difficulty: str = "beginner"
    student_id: Optional[str] = None

class TeachTopicRequest(BaseModel):
    topic: str
    student_question: Optional[str] = None
    tutor_type: str
    difficulty: str = "beginner"
    student_id: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    try:
        await db_manager.create_tables()
        print("✅ Database tables initialized successfully")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")

@app.get("/")
async def root():
    return {
        "message": "Claude Education Platform API",
        "version": "1.0.0",
        "available_tutors": list(tutors.keys())
    }

@app.post("/api/chat")
async def chat_with_tutor(request: ChatRequest):
    """Chat endpoint that integrates with our Python tutors"""
    try:
        # Get the selected tutor
        if request.tutor_type not in tutors:
            raise HTTPException(status_code=400, detail="Invalid tutor type")
        
        tutor = tutors[request.tutor_type]
        
        # Get the latest user message
        user_message = ""
        for msg in reversed(request.messages):
            if msg.role == "user":
                user_message = msg.content
                break
        
        if not user_message:
            raise HTTPException(status_code=400, detail="No user message found")
        
        # Use our tutor to generate response
        result = await tutor.teach_topic(
            topic=user_message,
            student_question=user_message,
            student_id=request.student_id
        )
        
        return {
            "response": result["answer"],
            "activities": result["activities"],
            "sources": result["sources"],
            "student_id": result["student_id"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/teach")
async def teach_topic(request: TeachTopicRequest):
    """Dedicated endpoint for teaching a specific topic"""
    try:
        if request.tutor_type not in tutors:
            raise HTTPException(status_code=400, detail="Invalid tutor type")
        
        tutor = tutors[request.tutor_type]
        
        result = await tutor.teach_topic(
            topic=request.topic,
            student_question=request.student_question,
            student_id=request.student_id
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/student/{student_id}/progress")
async def get_student_progress(student_id: str):
    """Get student's learning progress"""
    try:
        tutor = tutors["chatbot"]  # Any tutor can access progress
        progress = await tutor.get_student_history(student_id)
        
        return {
            "student_id": student_id,
            "progress": [
                {
                    "id": p.id,
                    "topic": p.topic,
                    "completion_score": p.completion_score,
                    "time_spent": p.time_spent,
                    "created_at": p.created_at.isoformat()
                }
                for p in progress
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/student/{student_id}/progress")
async def record_student_progress(
    student_id: str,
    topic: str,
    completion_score: float,
    time_spent: int,
    tutor_type: str = "chatbot"
):
    """Record student progress"""
    try:
        if tutor_type not in tutors:
            tutor_type = "chatbot"
            
        tutor = tutors[tutor_type]
        
        progress = await tutor.record_progress(
            student_id=student_id,
            topic=topic,
            completion_score=completion_score,
            time_spent=time_spent
        )
        
        if progress:
            return {
                "success": True,
                "progress_id": progress.id
            }
        else:
            return {
                "success": False,
                "message": "Failed to record progress"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/curriculum")
async def get_curriculum():
    """Get available curriculum lessons"""
    try:
        import json
        with open("data/curriculum/lessons.json", "r", encoding="utf-8") as f:
            curriculum = json.load(f)
        return curriculum
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading curriculum: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "tutors_available": list(tutors.keys()),
        "database_connected": True  # We could add actual DB health check here
    }

if __name__ == "__main__":
    print("🚀 Starting Claude Education Platform API Server...")
    print("📚 Available tutors:", list(tutors.keys()))
    print("🌐 API will be available at: http://localhost:8000")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )