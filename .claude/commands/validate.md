---
description: "Multi-phase validation for claude-education-platform"
---

# Validate claude-education-platform

Run comprehensive validation across all system components to ensure educational platform integrity.

## Phase 1: SDK Integration Check

**Purpose**: Verify all external API integrations are functional

```bash
cd /Users/tmkipper/Desktop/tk_projects/claude-education-platform
source venv/bin/activate
python test_sdks.py
```

**Expected Output**: ✅ 5/5 tests passing
- Environment variable configuration
- Claude SDK integration
- Firecrawl SDK v2 integration
- Database model initialization
- Tutor agent instantiation

**Multi-API Data Collection Validation**:
- Tavily: 3+ results for educational content search
- Exa: 3+ results for semantic content discovery
- Firecrawl: 5+ results for deep web scraping
- Total: 11+ sources per query

---

## Phase 2: Backend Code Quality

**Purpose**: Ensure Python code meets quality standards

```bash
source venv/bin/activate

# Code formatting check
black --check src/ config/ tests/

# Type checking
mypy src/ config/ --ignore-missing-imports
```

**Success Criteria**:
- No formatting errors
- No type errors (or only known/acceptable warnings)

---

## Phase 3: Frontend Lint & Build

**Purpose**: Validate Next.js frontend integrity

```bash
cd frontend

# ESLint check
npm run lint

# TypeScript compilation + production build
npm run build
```

**Success Criteria**:
- No linting errors
- Successful production build
- No TypeScript errors

---

## Phase 4: Unit Tests

**Purpose**: Run full test suite

```bash
cd /Users/tmkipper/Desktop/tk_projects/claude-education-platform
source venv/bin/activate

# Run all unit tests with verbose output
python -m pytest tests/ -v

# Optional: Run with coverage report
python -m pytest tests/ -v --cov=src --cov-report=term-missing
```

**Success Criteria**: All tests passing

---

## Phase 5: RAG System Check

**Purpose**: Verify ChromaDB and multi-API data collection working

```bash
source venv/bin/activate

# Run integration tests focusing on RAG
python test_integration.py
```

**Validation Points**:
- ChromaDB vector store accessible at `data/chroma_db/`
- Multi-API data collector functioning (Tavily + Exa + Firecrawl)
- Semantic search returning relevant results (distance < 0.7)
- Content deduplication working (MD5 hashing)

---

## Phase 6: Database Connectivity

**Purpose**: Ensure Neon PostgreSQL connection is active

```bash
source venv/bin/activate
python -c "from config.database import get_session; session = next(get_session()); print('✅ Neon PostgreSQL connected successfully')"
```

**Expected**: Connection to dark-heart-74010500 project successful

---

## Critical Educational Platform Rules

**ENFORCE THESE ALWAYS:**

1. **NO OpenAI models** - Use Anthropic Claude, Gemini, or Firecrawl only
2. **Cultural sensitivity** - All content appropriate for Mexican students
3. **Age-appropriate content** - Separate strategies for:
   - Ages 10-16: Simple explanations, visual examples
   - Ages 14-18: More technical depth, code samples
4. **API keys in `.env` only** - Never hardcode credentials
5. **Socratic method** - Guide discovery through questions, not direct answers
6. **Vercel deployment** - https://claude-education-platform-et9fb0qdy-scientia-capital.vercel.app

---

## Quick Validation Summary

**Green Light Checklist** (all must pass):
- [ ] test_sdks.py shows 5/5 passing
- [ ] No black formatting errors
- [ ] Frontend builds successfully
- [ ] All pytest tests passing
- [ ] RAG system returns results
- [ ] Neon database connected

**If any fail**: Review error output and fix before proceeding with development.

---

## Emergency Reset Commands

If validation fails catastrophically:

```bash
# Reset Python environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Reset frontend dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install

# Clear ChromaDB (WARNING: deletes all vector data)
rm -rf data/chroma_db

# Verify .env files exist
test -f .env && echo "✅ Backend .env exists" || echo "❌ Create .env from .env.example"
test -f frontend/.env && echo "✅ Frontend .env exists" || echo "❌ Create frontend/.env"
```

---

**Last Updated**: 2025-11-30
**Neon Project**: dark-heart-74010500
**Vercel URL**: https://claude-education-platform-et9fb0qdy-scientia-capital.vercel.app
