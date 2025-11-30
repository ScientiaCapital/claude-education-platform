---
description: "Execute a Project Requirements Plan (PRP) with 6-phase workflow"
---

# Execute PRP - Educational Platform Edition

Execute a previously generated PRP using a structured 6-phase workflow designed for multi-agent educational systems.

## Usage

```bash
/execute-prp [feature_name]
```

**Example**:
```bash
/execute-prp javascript-tutorial
```

This will load `PRPs/javascript_tutorial_PRP.md` and guide you through implementation.

---

## 6-Phase Execution Workflow

### Phase 1: Pre-Flight Validation

**Purpose**: Ensure system is ready for development

```bash
# Run full validation
/validate

# Verify PRP exists
ls PRPs/[feature_name]_PRP.md

# Activate environment
cd /Users/tmkipper/Desktop/tk_projects/claude-education-platform
source venv/bin/activate
```

**Checklist**:
- [ ] All 5/5 SDK tests passing
- [ ] PRP file exists and is complete
- [ ] Git working directory clean (or branch created)
- [ ] Environment variables configured
- [ ] Neon database connected

**DO NOT PROCEED** if validation fails. Fix issues first.

---

### Phase 2: Backend Implementation

**Purpose**: Implement tutor agents, RAG system, and database changes

#### Step 2.1: Database Schema Updates

```bash
# If PRP requires schema changes
cd /Users/tmkipper/Desktop/tk_projects/claude-education-platform

# Create migration script
echo "-- Migration: [feature_name]" > migrations/[timestamp]_[feature_name].sql

# Apply to Neon PostgreSQL
psql $DATABASE_URL -f migrations/[timestamp]_[feature_name].sql

# Verify
python -c "from config.database import get_session; session = next(get_session()); print('✅ Schema updated')"
```

#### Step 2.2: Tutor Agent Updates

```bash
# Edit affected tutor agents
# - src/agents/chatbot_tutor.py (for chatbot features)
# - src/agents/model_training_tutor.py (for ML features)
# - src/agents/programming_tutor.py (for coding features)

# Update system prompts with:
# 1. New educational objectives
# 2. Mexican cultural examples
# 3. Age-appropriate language
# 4. Socratic questioning patterns
```

**Critical Pattern**: Always use Socratic method
```python
# ✅ GOOD - Guides discovery
"¿Qué crees que pasaría si cambias el valor de esta variable?"

# ❌ BAD - Direct answer
"Debes cambiar la variable a 10."
```

#### Step 2.3: RAG System Enhancements

```bash
# Update knowledge base
python scripts/add_curriculum_content.py --topic [topic_name]

# Configure multi-API data collection
# Edit src/tools/data_collector.py to add new search patterns
```

**Multi-API Strategy**:
```python
# Use all three APIs strategically
tavily_results = await collector.search_tavily(query)      # 3 results - breadth
exa_results = await collector.search_exa(query)            # 3 results - semantics
firecrawl_results = await collector.scrape_firecrawl(url)  # 5 results - depth
# Total: 11 sources per query
```

#### Step 2.4: API Endpoint Creation

```bash
# Add FastAPI routes in api_server.py
# Follow pattern:
@app.post("/api/feature-name")
async def feature_endpoint(request: FeatureRequest):
    tutor = get_tutor(request.tutor_type)
    response = await tutor.get_response(request.message)
    return {"response": response, "metadata": {...}}
```

#### Step 2.5: Backend Testing

```bash
# Run unit tests
python -m pytest tests/ -v

# Test new tutor agent
python -m pytest tests/test_agents.py -v -k "test_[feature_name]"

# Test RAG system
python test_integration.py
```

**Success Criteria**: All tests passing

---

### Phase 3: Frontend Implementation

**Purpose**: Build user interfaces for both Streamlit (dev) and Next.js (prod)

#### Step 3.1: Streamlit Prototype (Development)

```bash
# Edit src/ui/app.py
# Add new sidebar option and page

# Test locally
streamlit run src/ui/app.py

# Navigate to new feature and verify:
# - Age-appropriate UI elements
# - Progress visualization works
# - Cultural examples display correctly
```

**Age-Appropriate UI Guidelines**:
- **Ages 10-16**: Large buttons, colorful, lots of visual feedback
- **Ages 14-18**: More compact, code editors, technical details visible

#### Step 3.2: Next.js Production Interface

```bash
cd frontend

# Create new component
mkdir -p src/components/[FeatureName]
touch src/components/[FeatureName]/[ComponentName].tsx

# Update API routes
# Edit src/app/api/[route]/route.ts

# Test locally
npm run dev

# Verify at http://localhost:3000
```

**Key Patterns**:
```typescript
// Use Vercel AI SDK for streaming
import { useChat } from 'ai/react';

export function TutorChat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/tutor/chat',
    body: { tutorType: 'programming' }
  });

  // Age-appropriate styling with Tailwind
  // Cultural color scheme (educational blues/greens)
}
```

#### Step 3.3: Frontend Testing

```bash
# Lint check
npm run lint

# Build test
npm run build

# Visual testing
npm run dev  # Manual testing in browser
```

---

### Phase 4: Cultural Adaptation & Testing

**Purpose**: Ensure content is culturally appropriate and age-suitable

#### Step 4.1: Cultural Review

**Checklist**:
- [ ] Mexican cultural examples used (e.g., "Taqueria ordering system" not "Pizza delivery")
- [ ] Language complexity appropriate for age group
- [ ] Encouragement patterns culturally sensitive
- [ ] No offensive or inappropriate content

**Example Cultural Adaptations**:
```python
# Ages 10-16 - Simple, visual
"Imagina que estás organizando una taqueria. ¿Cómo ordenarías los ingredientes?"

# Ages 14-18 - Technical
"Vamos a construir un sistema de gestión para una taqueria usando funciones JavaScript."
```

#### Step 4.2: Age-Appropriate Content Validation

```bash
# Test with sample queries for each age group
python scripts/test_age_appropriate_content.py --age-group 10-16
python scripts/test_age_appropriate_content.py --age-group 14-18
```

**Validation Criteria**:
- Vocabulary complexity matches age group
- Examples are relatable to Mexican students
- Learning pace is appropriate
- Technical depth matches capability

#### Step 4.3: Socratic Method Verification

**Test Conversation Flow**:
1. Student asks direct question → Tutor responds with guiding question
2. Student explores → Tutor provides gentle hints
3. Student discovers answer → Tutor celebrates with cultural encouragement
4. Student gets stuck → Tutor adjusts approach, doesn't give answer

**Example Session**:
```
Student: "¿Cómo hago un loop en Python?"
❌ BAD: "Usa 'for i in range(10):'"
✅ GOOD: "¿Qué quieres que tu programa repita? ¿Has visto cómo repetimos acciones en la vida diaria?"

Student: "Quiero repetir 'Hola' 5 veces"
✅ GOOD: "¡Perfecto! ¿Y si tuvieras que hacer eso manualmente, qué escribirías primero?"
```

---

### Phase 5: Integration Testing

**Purpose**: Ensure all components work together seamlessly

#### Step 5.1: Multi-Agent Flow Testing

```bash
# Test agent coordination (if feature uses multiple tutors)
python test_integration.py --test multi_agent_flow

# Verify:
# - Agent handoffs work correctly
# - Context is maintained across agents
# - Student progress tracked properly
```

#### Step 5.2: RAG System Validation

```bash
# Test knowledge augmentation
python test_integration.py --test rag_system

# Verify:
# - Tavily returns relevant educational content
# - Exa finds semantically similar resources
# - Firecrawl scrapes deep content correctly
# - Deduplication works (MD5 hashing)
# - Distance threshold triggers web research (> 0.7)
```

#### Step 5.3: End-to-End User Flow

```bash
# Test complete user journey
# 1. Student asks question
# 2. Tutor searches knowledge base
# 3. If insufficient, triggers web research
# 4. RAG enhancement occurs
# 5. Socratic response generated
# 6. Progress tracked in Neon database
# 7. Frontend displays appropriately

# Manual testing:
streamlit run src/ui/app.py
# Or
cd frontend && npm run dev
```

---

### Phase 6: Deployment & Documentation

**Purpose**: Ship to production and update documentation

#### Step 6.1: Pre-Deployment Checklist

```bash
# Full validation suite
/validate

# Verify critical requirements
- [ ] NO OpenAI models in code (grep -r "openai" src/)
- [ ] API keys only in .env files
- [ ] All tests passing (pytest + npm test)
- [ ] Frontend builds successfully
- [ ] Cultural adaptations reviewed
- [ ] Age-appropriate content validated
- [ ] Socratic method verified
```

#### Step 6.2: Vercel Deployment

```bash
# Build frontend
cd frontend
npm run build

# Test production build locally
npm run start

# Deploy to Vercel (if auto-deploy not configured)
vercel --prod

# Verify at: https://claude-education-platform-et9fb0qdy-scientia-capital.vercel.app
```

#### Step 6.3: Database Migration (Neon)

```bash
# If schema changes were made
# Ensure migration already applied to Neon PostgreSQL (dark-heart-74010500)

# Verify in production
NEON_DATABASE_URL=$DATABASE_URL python -c "from config.database import get_session; session = next(get_session()); print('✅ Production DB ready')"
```

#### Step 6.4: Documentation Updates

**Files to Update**:

1. **CLAUDE.md** (root project guide)
   - Add feature to "Current Status" section
   - Update architecture overview if needed
   - Note any new environment variables

2. **PLANNING.md** (architecture decisions)
   - Document design decisions made during implementation
   - Add new educational patterns discovered
   - Update data flow diagrams if needed

3. **TASK.md** (current work tracking)
   - Mark feature as complete
   - Note any follow-up tasks
   - Update production status

4. **README.md** (if user-facing changes)
   - Add feature to feature list
   - Update usage examples
   - Include screenshots if UI changed

#### Step 6.5: Git Commit & Tag

```bash
# Add all changes
git add .

# Commit with descriptive message
git commit -m "feat(education): Add [feature_name] with Socratic method

- Updated [tutor_agent] with new prompts
- Enhanced RAG system with [API] integration
- Added age-appropriate UI for [age_group]
- Included Mexican cultural examples
- All tests passing (5/5 SDK + unit + integration)

Refs: PRPs/[feature_name]_PRP.md"

# Tag release
git tag -a v[version] -m "Release: [feature_name]"

# Push to GitHub
git push origin main
git push origin --tags
```

---

## Post-Execution Validation

After completing all 6 phases, run final validation:

```bash
# Full system check
/validate

# Verify in production
curl https://claude-education-platform-et9fb0qdy-scientia-capital.vercel.app/api/health

# Test new feature in production
# - Navigate to deployed URL
# - Test with both age groups (10-16, 14-18)
# - Verify cultural examples display
# - Ensure Socratic method works
# - Check progress tracking
```

**Success Criteria**:
- [ ] All validation tests pass
- [ ] Feature works in production
- [ ] Documentation updated
- [ ] No OpenAI models detected
- [ ] Cultural adaptation verified
- [ ] Age-appropriate content confirmed

---

## Rollback Procedure

If something goes wrong in production:

```bash
# Revert to previous commit
git revert HEAD

# Push revert
git push origin main

# Vercel auto-deploys the revert

# Or manual rollback in Vercel dashboard
# Navigate to Deployments → Select previous working deployment → Promote to Production
```

---

## Critical Educational Platform Rules

**MUST ENFORCE DURING EXECUTION:**

1. **NO OpenAI models** - Use Anthropic Claude, Gemini, or Firecrawl only
2. **Age-appropriate content** - Test with both 10-16 and 14-18 age groups
3. **Cultural sensitivity** - Mexican cultural references required, review before deployment
4. **Socratic method** - Guide discovery, never give direct answers
5. **API keys in .env only** - Never hardcode, check before commit
6. **Multi-API data collection** - Use all three: Tavily + Exa + Firecrawl
7. **Dual interface support** - Test both Streamlit (dev) and Next.js (prod)
8. **Progress tracking** - Ensure Neon database records student progress

---

## Troubleshooting Common Issues

### Issue: SDK Tests Failing

```bash
# Check environment variables
python -c "from config.settings import settings; print(settings.anthropic_api_key[:10])"

# Reinstall dependencies
pip install -r requirements.txt

# Re-run tests
python test_sdks.py
```

### Issue: Frontend Won't Build

```bash
cd frontend
rm -rf node_modules package-lock.json .next
npm install
npm run build
```

### Issue: RAG System Not Finding Results

```bash
# Check ChromaDB
ls -la data/chroma_db/

# Verify API keys
echo $TAVILY_API_KEY
echo $EXA_API_KEY
echo $FIRECRAWL_API_KEY

# Test data collector directly
python -c "from src.tools.data_collector import DataCollector; collector = DataCollector(); print(collector.search_tavily('Python tutorial'))"
```

### Issue: Database Connection Failed

```bash
# Check Neon connection string
echo $DATABASE_URL

# Test connection
python -c "from config.database import get_session; session = next(get_session()); print('Connected')"

# Verify Neon project status at: https://console.neon.tech/app/projects/dark-heart-74010500
```

---

**Last Updated**: 2025-11-30
**Neon Project**: dark-heart-74010500
**Vercel URL**: https://claude-education-platform-et9fb0qdy-scientia-capital.vercel.app
