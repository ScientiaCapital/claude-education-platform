# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
# Backend setup
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd frontend && npm install

# Environment configuration
cp .env.example .env  # Configure with your API keys
cd frontend && cp .env.example .env
```

### Running the Platform
```bash
# Test SDK integrations and configuration
python test_sdks.py

# Option 1: Streamlit interface (recommended for development)
streamlit run src/ui/app.py

# Option 2: Full-stack (FastAPI + Next.js)
python api_server.py  # Terminal 1 (backend on :8000)
cd frontend && npm run dev  # Terminal 2 (frontend on :3000)

# Quick demo
python examples/quick_start.py
```

### Testing and Quality
```bash
# Run integration tests
python -m pytest tests/ -v

# Frontend linting and building
cd frontend && npm run lint
cd frontend && npm run build

# Database operations (if using Drizzle with frontend)
cd frontend && npm run db:generate
cd frontend && npm run db:migrate
```

## Architecture Overview

### Core Educational System
The platform implements a multi-agent educational system with three specialized AI tutors that use the Socratic method for teaching programming and AI concepts to Mexican students (ages 10-18).

**Key Components:**
- **EducationalTutor Base Class** (`src/agents/tutor_agent.py`): Implements Socratic teaching methodology with cultural context
- **Specialized Tutors**: ChatbotTutor, ModelTrainingTutor, ProgrammingTutor - each with domain-specific prompts and examples
- **RAG System** (`src/rag/`): ChromaDB vector storage + multi-API data collection for dynamic knowledge augmentation
- **Data Collector** (`src/tools/data_collector.py`): Unified interface for Firecrawl, Exa, and Tavily APIs

### Data Flow Architecture
1. **Student Query** → **Tutor Agent** → **Knowledge Base Search**
2. If insufficient context → **Data Collector** (web research) → **Knowledge Base Update**
3. **RAG-Enhanced Response** → **Socratic Enhancement** → **Student Response** + **Progress Tracking**

### Database Schema (Neon PostgreSQL)
- **StudentProgress**: Track completion scores, time spent, topics covered
- **LessonContent**: Structured curriculum with difficulty levels and categories
- **StudentInteraction**: Conversation history with satisfaction ratings

### Frontend Architecture
**Dual Interface Strategy:**
- **Streamlit** (`src/ui/app.py`): Feature-complete development interface with progress visualization
- **Next.js** (`frontend/`): Production-ready interface using Vercel AI SDK for streaming responses

**API Bridge**: FastAPI server (`api_server.py`) exposes Python tutors as REST endpoints for frontend consumption.

## Configuration Management

### Settings System
Central configuration through `config/settings.py` using Pydantic settings:
- **API Keys**: All external service credentials
- **Model Parameters**: Claude model selection, temperature, token limits
- **RAG Configuration**: Chunk sizes, overlap, similarity thresholds
- **Neon Project ID**: Hardcoded as "dark-heart-74010500"

### Required Environment Variables
```env
ANTHROPIC_API_KEY=     # Primary AI model
FIRECRAWL_API_KEY=     # Web scraping
DATABASE_URL=          # Neon PostgreSQL connection
EXA_API_KEY=          # Semantic search (optional)
TAVILY_API_KEY=       # Research API (optional)
```

## Educational Methodology

### Socratic Teaching Implementation
Each tutor implements cultural-specific prompts that:
- Guide discovery through questions rather than direct answers
- Use Mexican cultural references and local examples
- Adapt language complexity based on age groups (10-16, 14-18)
- Celebrate progress and maintain encouragement

### Curriculum Structure
Predefined lessons in `data/curriculum/lessons.json` with:
- **Age-appropriate content** (10-16 and 14-18 year ranges)
- **Progressive difficulty** (beginner → intermediate → advanced)
- **Hands-on activities** designed for 15-30 minute engagement
- **Cultural relevance** (tacos vs quesadillas for ML examples, Mexican brands for chatbot scenarios)

### Knowledge Augmentation Strategy
The RAG system dynamically enhances lessons by:
1. **Semantic search** of existing knowledge base
2. **Automatic web research** when context is insufficient (distance > 0.7)
3. **Content deduplication** using MD5 hashing
4. **Multi-source aggregation** (Tavily for comprehensive info, Exa for semantic similarity, Firecrawl for deep scraping)

## Development Notes

### Python Virtual Environment Usage
Always activate the virtual environment when running Python components:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### API Integration Testing
Use `test_sdks.py` to verify all external integrations before development. The script provides comprehensive validation of:
- Environment variable configuration
- API key validity and connectivity
- Database model initialization
- Tutor agent instantiation

### Database Integration
The platform uses dual database strategies:
- **ChromaDB**: Local vector storage for RAG (persistent at `data/chroma_db/`)
- **Neon PostgreSQL**: Student progress and interaction tracking (serverless, branching-capable)

### Frontend Development
The Next.js frontend uses Server-Side Rendering with API routes that proxy to the Python backend. Key patterns:
- **useChat hook** from Vercel AI SDK for streaming responses
- **Tailwind CSS** with custom education-themed color palette
- **Framer Motion** for engaging animations appropriate for younger users