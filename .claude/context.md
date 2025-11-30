```markdown
# Claude Education Platform - Project Context

**Last Updated:** 2025-10-31T13:04:05.086548

## Current Sprint & Focus Areas 🎯

**Primary Focus:** Platform Foundation & Core AI Tutor Development
- **Sprint Goal:** Establish working AI tutor system with multiple specialized tutors
- **Key Areas:**
  - Backend API development with FastAPI
  - AI tutor specialization (Chatbots, ML, Programming)
  - Frontend integration with Next.js and Streamlit
  - Database setup with Neon PostgreSQL
  - MCP integration for AI tooling

## Architecture Overview 🏗️

- **Language:** Python
- **Framework:** FastAPI
- **Project Type:** AI/ML Education Platform
- **Frontend Options:** Streamlit & Next.js with Vercel AI SDK
- **Database:** Neon PostgreSQL (Serverless)
- **AI Integration:** Anthropic Claude, Firecrawl, Exa, Tavily

## Project Description 📖

The Claude Education Platform is an AI-powered educational system designed to teach programming and artificial intelligence concepts to children and teenagers in Mexico. The platform features three specialized AI tutors, each focusing on different technical domains: chatbot development, machine learning training, and Python programming applied to AI.

Using a Socratic teaching methodology, the tutors guide students through interactive learning experiences with culturally relevant content and examples from Mexican context. The platform incorporates intelligent RAG (Retrieval-Augmented Generation) systems with multiple data sources and provides flexible interfaces through both Streamlit and Next.js frontends, backed by a serverless PostgreSQL database for scalable educational experiences.

## Recent Changes 📋

**Initial Project Generation (2025-10-31)**
- ✅ Project structure established
- ✅ FastAPI backend framework configured
- ✅ Multi-tutor AI system designed
- ✅ Frontend options (Streamlit + Next.js) planned
- ✅ Database integration (Neon PostgreSQL) configured
- ✅ MCP tooling integration prepared
- ✅ API key management system outlined

## Current Blockers 🚧

*None identified - project in initial setup phase*

## Next Steps 🚀

1. **Immediate Setup (This Week)**
   - Configure all required API keys in environment files
   - Set up Neon PostgreSQL database connection
   - Implement basic FastAPI endpoints for tutor interactions

2. **Core Development (Next 2 Weeks)**
   - Build the three specialized tutor classes with Claude integration
   - Implement RAG system with Firecrawl for content retrieval
   - Create basic Streamlit interface for tutor interactions

3. **Testing & Validation**
   - Run `test_sdks.py` to verify all integrations
   - Test each tutor with sample educational content
   - Validate Socratic questioning methodology

4. **Frontend Development**
   - Set up Next.js frontend with Vercel AI SDK
   - Implement user session management
   - Create culturally relevant Mexican examples and content

## Development Workflow 🔄

### Backend Development
```bash
# Activate environment
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Run development server
uvicorn main:app --reload

# Test integrations
python test_sdks.py
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Database Management
- Use Neon PostgreSQL for serverless data storage
- Environment variables configured in `.env`
- Connection testing via `test_sdks.py`

### API Key Requirements
- Anthropic (Claude) - Required
- Firecrawl - Required  
- Exa - Optional
- Tavily - Optional
- Neon Database - Required

## Notes 📝

### Cultural Context
- Content tailored for Mexican students
- Examples using local references and contexts
- Spanish language support planned

### AI Tutor Specializations
1. **Chatbot Tutor** 🤖 - Intelligent chatbot creation
2. **AI Tutor** 🧠 - Machine learning model training  
3. **Programming Tutor** 💻 - Python applied to AI

### Integration Priorities
1. Claude API + FastAPI backend
2. RAG system with Firecrawl
3. Streamlit interface (quicker deployment)
4. Next.js frontend (production ready)

### Testing Strategy
- SDK testing via `test_sdks.py`
- Tutor response validation
- Cultural relevance review
- Performance testing with multiple students
```