# CLAUDE.md - Claude Education Platform

## 1. Project Status & Overview

**Current Status**: Active Development 🚧  
**Project Type**: AI-Powered Educational Platform  
**Target Audience**: Children and adolescents in Mexico learning programming and AI concepts

The Claude Education Platform is a specialized learning environment featuring three AI tutors:
- **🤖 Chatbot Tutor**: Teaches intelligent chatbot creation
- **🧠 AI Tutor**: Trains machine learning models  
- **💻 Programming Tutor**: Python applied to AI

**Key Methodologies**:
- Socratic teaching approach through guided questioning
- Culturally relevant content with Mexican references
- Multi-source RAG (Retrieval Augmented Generation) system
- Multiple interface options (Streamlit + Next.js)

## 2. Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **AI/ML Core**: 
  - `anthropic` - Claude API integration
  - `langchain` - AI workflow orchestration
  - `firecrawl-py` - Web content extraction
  - `exa-py` - Search enhancement (optional)
  - `tavily-python` - Web search (optional)

### Frontend Options
- **Streamlit**: Rapid prototyping and admin interfaces
- **Next.js** with Vercel AI SDK: Production web interface

### Database
- **Neon PostgreSQL**: Serverless PostgreSQL with branching

### Development Tools
- Testing: pytest
- Environment Management: python-dotenv
- API Documentation: Auto-generated FastAPI docs

## 3. Development Workflow

### Initial Setup
```bash
# Clone and setup
git clone https://github.com/ScientiaCapital/claude-education-platform.git
cd claude-education-platform

# Backend setup
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys

# Frontend setup (if using Next.js)
cd frontend
npm install
cp .env.example .env
cd ..
```

### Running the Application

**Backend (FastAPI)**
```bash
# Development server with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Streamlit Interface**
```bash
streamlit run streamlit_app.py
```

**Next.js Frontend**
```bash
cd frontend
npm run dev
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_tutors.py

# Run with coverage
pytest --cov=app tests/

# Test SDK connectivity (initial verification)
python test_sdks.py
```

### Building
```bash
# Install production dependencies
pip install -r requirements.txt

# Generate API documentation
# Automatically available at /docs when running FastAPI
```

## 4. Environment Variables

Create a `.env` file in the project root:

```env
# Required - Core AI Services
ANTHROPIC_API_KEY=your_anthropic_key_here
FIRECRAWL_API_KEY=your_firecrawl_key_here

# Optional - Enhanced Search
EXA_API_KEY=your_exa_key_here
TAVILY_API_KEY=your_tavily_key_here

# Database
DATABASE_URL=your_neon_postgresql_connection_string

# Application Settings
APP_ENV=development
LOG_LEVEL=INFO
MAX_TOKENS=4000
TEMPERATURE=0.7

# Frontend (in frontend/.env)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 5. Key Files & Their Purposes

### Core Application
- `main.py` - FastAPI application entry point
- `app/tutors/` - Tutor implementations (chatbot, ai, programming)
- `app/rag/` - Retrieval Augmented Generation system
- `app/models/` - Data models and Pydantic schemas

### Configuration
- `mcp-config.json` - Model Context Protocol configuration for Claude Code
- `requirements.txt` - Python dependencies
- `test_sdks.py` - Initial API connectivity verification

### Frontend
- `streamlit_app.py` - Streamlit interface
- `frontend/` - Next.js application with Vercel AI SDK

### Testing
- `tests/` - pytest test suites
- `tests/test_tutors.py` - Tutor functionality tests
- `tests/test_rag.py` - RAG system tests

## 6. Testing Approach

### Test Structure
```python
# Example test pattern
def test_chatbot_tutor_response():
    """Test that chatbot tutor provides educational responses"""
    tutor = ChatbotTutor()
    response = tutor.ask_question("¿Qué es un chatbot?")
    assert "chatbot" in response.lower()
    assert len(response) > 0
```

### Test Categories
- **Unit Tests**: Individual tutor methods and RAG components
- **Integration Tests**: API endpoints and database interactions
- **SDK Tests**: External API connectivity (Anthropic, Firecrawl, etc.)

### Running Tests
```bash
# Complete test suite
pytest

# Specific test category
pytest tests/ -m "not slow"  # Skip slow integration tests

# Generate test report
pytest --html=report.html --self-contained-html
```

## 7. Deployment Strategy

### Backend Deployment Options
**Option 1: Cloud Provider**
```bash
# Example for deployment to cloud platform
# Ensure all environment variables are set in production
```

**Option 2: Containerized (Future)**
```dockerfile
# When Docker support is added
FROM python:3.9-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Deployment
```bash
# Next.js deployment to Vercel
cd frontend
vercel --prod
```

### Database
- **Neon PostgreSQL**: Automatic scaling with branch-based environments
- Connection pooling enabled for production workloads

## 8. Coding Standards

### Python Standards
- **Style**: Black formatter, flake8 for linting
- **Type Hints**: Required for all function signatures
- **Docstrings**: Google style for all public methods

```python
def teach_concept(self, concept: str, student_level: StudentLevel) -> TeachingResponse:
    """Teach a specific AI concept using Socratic method.
    
    Args:
        concept: The AI concept to teach
        student_level: Student's current understanding level
        
    Returns:
        TeachingResponse: Structured teaching response with questions
    """
```

### AI-Specific Standards
- **Prompt Engineering**: All prompts in separate templates/files
- **Error Handling**: Graceful degradation when AI services are unavailable
- **Token Management**: Respect context window limits with summarization

### Cultural Relevance
- Include Mexican cultural references in examples
- Spanish language support with proper localization
- Culturally appropriate learning examples

## 9. Common Tasks & Commands

### Development
```bash
# Start development environment
./scripts/dev.sh  # Or manually start backend + frontend

# Check API health
curl http://localhost:8000/health

# Test tutor responses
python -c "from app.tutors.chatbot import ChatbotTutor; print(ChatbotTutor().introduce())"
```

### Database Operations
```bash
# Database migrations (when implemented)
alembic upgrade head

# Seed initial data
python scripts/seed_data.py
```

### Maintenance
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Clean __pycache__
find . -name "__pycache__" -exec rm -rf {} +
```

## 10. Troubleshooting Tips

### Common Issues

**API Connection Problems**
```bash
# Test Anthropic connection
python -c "import anthropic; client = anthropic.Anthropic(api_key='your_key'); print(client.models.list())"

# Test Firecrawl
python test_sdks.py
```

**Module Import Errors**
- Ensure you're in the correct virtual environment
- Check that `app` is in Python path: `export PYTHONPATH=.`

**Frontend-Backend Connection**
- Verify both servers are running on correct ports
- Check CORS settings in FastAPI app
- Confirm API URLs in frontend environment variables

**Performance Issues**
- Monitor token usage in Anthropic responses
- Implement response caching for frequent queries
- Use RAG system to reduce context window usage

### Debug Mode
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Or set in environment
APP_ENV=development
LOG_LEVEL=DEBUG
```

### Getting Help
- Check FastAPI auto-generated docs at `/docs`
- Review test cases for usage examples
- Examine `test_sdks.py` for API connectivity patterns

---

*This CLAUDE.md file will evolve as the project grows. Update it when adding new features or changing architecture.*