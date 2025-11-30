# Claude Education Platform - Architecture Documentation

## 1. Technology Stack

### Backend Framework
- **FastAPI** 0.104+ (Python web framework with automatic OpenAPI documentation)
- **Python** 3.9+ (Primary programming language)
- **Uvicorn** (ASGI server for FastAPI)

### AI/ML Components
- **Anthropic Claude** (via `anthropic` SDK) - Primary LLM
- **LangChain** + **langchain-anthropic** - AI orchestration framework
- **RAG System** - Multi-source retrieval augmented generation

### Data Processing & Storage
- **ChromaDB** - Vector database for embeddings and semantic search
- **Neon PostgreSQL** - Serverless relational database
- **Pandas** + **NumPy** - Data manipulation and numerical computing

### Search & Web Scraping
- **Firecrawl-py** - Web scraping and content extraction
- **Exa-py** - Neural search API
- **Tavily-python** - AI-powered search API

### Frontend Interfaces
- **Streamlit** - Rapid prototyping and educational interface
- **Next.js 14+** with **Vercel AI SDK** - Production web interface
- **React** - Frontend framework

### Development & Testing
- **Pytest** - Testing framework
- **MCP (Model Context Protocol)** - Tool integration protocol

## 2. Design Patterns

### Architectural Patterns
- **Microservices Architecture**: Separate backend (FastAPI) and frontend (Streamlit/Next.js)
- **Repository Pattern**: Data access abstraction for multiple data sources
- **Strategy Pattern**: Multiple AI tutors with specialized behaviors
- **Observer Pattern**: Real-time updates between AI processing and UI

### AI/ML Patterns
- **RAG (Retrieval-Augmented Generation)**: Enhanced AI responses with external knowledge
- **Chain-of-Thought**: Socratic teaching methodology implementation
- **Agent Pattern**: Specialized tutor agents with specific capabilities
- **Pipeline Pattern**: Sequential data processing through multiple AI components

### API Patterns
- **RESTful API Design**: Resource-oriented endpoints in FastAPI
- **WebSocket Connections**: Real-time communication for AI interactions
- **Dependency Injection**: FastAPI's built-in dependency management

## 3. Key Components

### Core Application Components

#### AI Tutor System
```python
class TutorManager:
    - ChatbotTutor: 🤖 Specialized in chatbot creation
    - AITutor: 🧠 Machine learning model training
    - ProgrammingTutor: 💻 Python applied to AI
```

#### RAG Engine
- **Document Processor**: Handles multiple data sources (Firecrawl, Exa, Tavily)
- **Vector Store**: ChromaDB for semantic search and embeddings
- **Query Router**: Determines optimal data source for queries

#### Content Management
- **Cultural Context Engine**: Mexican cultural relevance processor
- **Curriculum Manager**: Educational content organization
- **Progress Tracker**: Student learning progress monitoring

#### API Layer
- **FastAPI Application**: Main backend server
- **WebSocket Manager**: Real-time AI interactions
- **Authentication Service**: User management and security

### Frontend Components
- **Streamlit Dashboard**: Educational interface for students
- **Next.js Application**: Production web interface
- **Vercel AI SDK Integration**: AI chat components

## 4. Data Flow

### Typical User Interaction Flow
1. **User Input** → Frontend (Streamlit/Next.js)
2. **Request Routing** → FastAPI Backend
3. **Tutor Selection** → TutorManager routes to specialized tutor
4. **Query Processing** → RAG Engine retrieves relevant information
5. **Multi-source Retrieval** → Firecrawl/Exa/Tavily APIs
6. **Context Augmentation** → Cultural relevance processing
7. **AI Generation** → Anthropic Claude with augmented context
8. **Response Delivery** → WebSocket/HTTP response to frontend
9. **Progress Tracking** → Database update for learning analytics

### RAG Data Flow
```
User Query → Query Understanding → Source Selection → 
→ Document Retrieval → Vector Search (ChromaDB) → 
→ Context Assembly → Prompt Engineering → 
→ Claude Generation → Response Delivery
```

## 5. External Dependencies

### AI/ML Dependencies
```python
anthropic>=0.7.0          # Claude API client
langchain>=0.0.350        # AI orchestration framework
langchain-anthropic>=0.0.2 # LangChain Claude integration
```

### Search & Data Dependencies
```python
firecrawl-py>=0.0.5       # Web scraping and content extraction
exa-py>=0.0.8             # Neural search API
tavily-python>=0.1.0      # AI-powered search
chromadb>=0.4.0           # Vector database for embeddings
```

### Web Framework Dependencies
```python
fastapi>=0.104.0          # Web framework
uvicorn>=0.24.0           # ASGI server
streamlit>=1.28.0         # Frontend interface
```

### Data Processing
```python
pandas>=2.0.0             # Data manipulation
numpy>=1.24.0             # Numerical computing
```

### Database
```python
asyncpg>=0.28.0           # Async PostgreSQL driver
sqlalchemy>=2.0.0         # SQL toolkit and ORM
```

## 6. API Design

### FastAPI Endpoints Structure

#### Core API Routes
```python
# Tutor Management
POST /api/tutors/{tutor_type}/chat
GET  /api/tutors/available
POST /api/tutors/session/start
POST /api/tutors/session/end

# Content Management
GET  /api/content/curriculum
POST /api/content/search
GET  /api/content/cultural/{topic}

# User Management
POST /api/users/register
POST /api/users/login
GET  /api/users/progress
```

#### WebSocket Routes
```python
# Real-time AI interactions
WS   /ws/tutors/{tutor_type}
WS   /ws/progress/updates
```

#### RAG System Endpoints
```python
POST /api/rag/search        # Multi-source search
POST /api/rag/context       # Context retrieval
GET  /api/rag/sources       # Available data sources
```

### Request/Response Schema
```python
class TutorRequest(BaseModel):
    message: str
    tutor_type: Literal["chatbot", "ai", "programming"]
    session_id: Optional[str]
    cultural_context: str = "mexican"

class TutorResponse(BaseModel):
    response: str
    session_id: str
    sources: List[Dict]
    cultural_references: List[str]
```

## 7. Database Schema

### Neon PostgreSQL Tables

#### Users & Progress Tracking
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    age_group VARCHAR(50) NOT NULL, -- 'children', 'teenagers'
    created_at TIMESTAMPTZ DEFAULT NOW(),
    cultural_preferences JSONB DEFAULT '{}'
);

CREATE TABLE learning_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    tutor_type VARCHAR(50) NOT NULL,
    start_time TIMESTAMPTZ DEFAULT NOW(),
    end_time TIMESTAMPTZ,
    messages JSONB DEFAULT '[]'
);

CREATE TABLE student_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    skill_category VARCHAR(100) NOT NULL,
    proficiency_level INTEGER DEFAULT 1,
    last_updated TIMESTAMPTZ DEFAULT NOW()
);
```

#### Content & Knowledge Base
```sql
CREATE TABLE educational_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    content_type VARCHAR(100), -- 'example', 'exercise', 'theory'
    difficulty_level INTEGER,
    cultural_context VARCHAR(100) DEFAULT 'mexican',
    tags TEXT[],
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE rag_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type VARCHAR(50), -- 'firecrawl', 'exa', 'tavily'
    url VARCHAR(1000),
    content_hash VARCHAR(64),
    last_crawled TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}'
);
```

### ChromaDB Collections
- `educational_embeddings`: Vector store for educational content
- `cultural_contexts`: Mexican cultural references and examples
- `code_examples`: Programming examples with embeddings

## 8. Security Considerations

### FastAPI Security
```python
# JWT Authentication
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer()

# CORS Configuration
from fastapi.middleware.cors import CORSMiddleware

# Rate Limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
```

### API Key Management
- Environment variable storage for all external API keys
- Secure key rotation policies
- API usage monitoring and quotas

### Data Security
- **PII Protection**: Minimal user data collection
- **Data Encryption**: At-rest and in-transit encryption
- **Access Controls**: Role-based access for different tutor types

### AI Security
- **Prompt Injection Protection**: Input validation and sanitization
- **Content Filtering**: Output moderation for educational content
- **Usage Limits**: Prevent API abuse through rate limiting

## 9. Performance Optimization

### Caching Strategies
```python
# Redis for session caching
import redis.asyncio as redis

# Vector cache for frequent queries
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_embedding(query: str) -> List[float]:
    pass
```

### Database Optimization
- **Connection Pooling**: Async database connections
- **Indexed Queries**: Proper indexing on frequently queried columns
- **Query Optimization**: Efficient joins and query patterns

### AI Performance
- **Prompt Optimization**: Efficient token usage with Claude
- **Batch Processing**: Group similar requests
- **Response Streaming**: Progressive delivery of AI responses

### Frontend Performance
- **Static Generation**: Next.js static site generation where possible
- **Code Splitting**: Lazy loading of AI components
- **CDN Integration**: Content delivery network for static assets

## 10. Deployment Strategy

### Current Deployment (No Docker)
```bash
# Backend Deployment
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Streamlit Deployment
streamlit run app.py --server.port 8501

# Next.js Deployment
npm run build && npm start
```

### Recommended Deployment Architecture

#### Development Environment
```yaml
# Backend: Local development with hot reload
uvicorn main:app --reload --host localhost --port 8000

# Frontend: Next.js development server
npm run dev

# Database: Neon PostgreSQL with connection pooling
```

#### Production Deployment
1. **Backend**: Deploy FastAPI to cloud platform (Railway, Heroku, AWS)
2. **Frontend**: Vercel deployment for Next.js application
3. **Database**: Neon PostgreSQL with automated backups
4. **Vector Store**: ChromaDB with persistent storage
5. **CDN**: Cloudflare for static assets and caching

### Monitoring & Logging
- **Application Metrics**: Response times, error rates, API usage
- **AI Performance**: Token usage, response quality, latency
- **User Analytics**: Learning progress, engagement metrics

### Scaling Considerations
- **Horizontal Scaling**: Multiple backend instances with load balancing
- **Database Scaling**: Read replicas for PostgreSQL
- **Cache Layer**: Redis for session storage and frequent queries
- **CDN**: Global content delivery for educational materials

This architecture supports the educational platform's goals of providing culturally relevant AI-powered education while maintaining performance, security, and scalability for Mexican students learning programming and AI concepts.