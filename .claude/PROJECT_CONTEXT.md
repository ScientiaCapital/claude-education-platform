# claude-education-platform

**Branch**: main | **Updated**: 2025-11-30

## Status
Multi-agent educational system with three specialized AI tutors using Socratic method for teaching programming and AI concepts to Mexican students (ages 10-18). All 5/5 SDK tests passing. Frontend deployed on Vercel with complete API integration.

## Today's Focus
1. [ ] (Add today's tasks here)

## Done (This Session)
- (none yet)

## Critical Rules
- **NO OpenAI models** - Use Anthropic Claude only
- API keys in `.env` only, never hardcoded
- All external service credentials managed through Pydantic settings

## Blockers
(none)

## Quick Commands
```bash
source venv/bin/activate
streamlit run src/ui/app.py              # Development UI
python api_server.py                      # FastAPI backend (port 8000)
cd frontend && npm run dev                # Next.js frontend (port 3000)
python -m pytest tests/ -v                # Run tests
python test_sdks.py                       # Verify API integrations (5/5 passing)
```

## Tech Stack
- **Backend**: Python 3.11+, FastAPI, ChromaDB (RAG), SQLAlchemy
- **Database**: Neon PostgreSQL (dark-heart-74010500)
- **Frontend**: Next.js 14, Vercel AI SDK, Tailwind CSS, Framer Motion
- **AI**: Anthropic Claude (primary), Multi-API data collection (Firecrawl, Exa, Tavily)
- **Deployment**: Vercel (https://claude-education-platform-et9fb0qdy-scientia-capital.vercel.app)

## Recent Commits
- bf9a6ef Fix async/sync database integration and improve error handling
- 11bd621 Fix Vercel deployment configuration
- cb7da6a Fix Vercel deployment and test configurations
