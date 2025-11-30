# PRP Template: [Feature Name]

**Generated**: [Date]
**Author**: [Name]
**Status**: Draft | In Progress | Complete
**Priority**: Low | Medium | High | Critical

---

## Executive Summary

**Purpose**: [One sentence describing what this feature achieves for students]

**Target Age Group**:
- [ ] Ages 10-16 (Simple explanations, visual examples)
- [ ] Ages 14-18 (Technical depth, code samples)
- [ ] Both age groups (with adaptation)

**Complexity**: Low | Medium | High

**Estimated Effort**: Small (1-2 days) | Medium (3-5 days) | Large (1-2 weeks)

**Educational Impact**: [How this improves learning outcomes]

---

## Educational Objectives

### Learning Outcomes

After completing this feature, students will be able to:

1. [Specific, measurable learning outcome 1]
2. [Specific, measurable learning outcome 2]
3. [Specific, measurable learning outcome 3]

### Socratic Teaching Approach

**Guiding Questions Pattern**:
```
Student Query: [Example student question]

Tutor Response (Socratic):
1. [Probing question to assess understanding]
2. [Follow-up to guide discovery]
3. [Hint if student is stuck - not direct answer]
4. [Celebration when student discovers answer]
```

**Example Conversation Flow**:
```
Student: "¿Cómo funciona un loop en Python?"

❌ AVOID (Direct Answer):
"Un loop usa 'for' o 'while' para repetir código."

✅ USE (Socratic Method):
"¡Buena pregunta! Antes de aprender sobre loops, dime: ¿qué actividades repites
todos los días? Por ejemplo, ¿te lavas los dientes una vez o varias veces?"

[Student responds]

"¡Exacto! Así como repites acciones en la vida, Python puede repetir
instrucciones. ¿Qué crees que necesitaríamos decirle a Python para que repita algo?"
```

---

## Cultural Context

### Mexican Cultural Examples

**Primary Examples**:
1. [Cultural reference 1 - e.g., "Taqueria ordering system"]
2. [Cultural reference 2 - e.g., "Día de los Muertos calendar"]
3. [Cultural reference 3 - e.g., "Lucha libre roster management"]

**Why These Work**:
- Relatable to Mexican students' daily life
- Engaging and culturally relevant
- Provides concrete context for abstract concepts

### Language Complexity

**For Ages 10-16**:
- Simple vocabulary (avoid: "algoritmo", use: "pasos a seguir")
- Short sentences
- Lots of visual analogies ("como cuando...")
- Celebratory language ("¡Excelente!", "¡Lo lograste!")

**For Ages 14-18**:
- Technical terminology with explanations
- More complex sentence structures
- Code examples with detailed comments
- Professional tone with encouragement

### Encouragement Patterns

**Cultural Celebrations**:
- "¡Muy bien! Estás pensando como un programador."
- "¡Eso es! Descubriste el patrón tú mismo/a."
- "¡Excelente razonamiento! Así es como resolvemos problemas complejos."

---

## Technical Architecture

### Affected Tutor Agents

**Primary Tutor**: [ChatbotTutor | ModelTrainingTutor | ProgrammingTutor | New Tutor]

**System Prompt Updates**:
```python
# Update in: src/agents/[tutor_name].py

NEW_SYSTEM_PROMPT = """
[Educational objective for this feature]

Your role:
- Guide students using Socratic method
- Use Mexican cultural examples: [list examples]
- Adapt language for [age group]
- Never give direct answers - ask guiding questions
- Celebrate discoveries with cultural encouragement

Example interaction:
[Paste example conversation from "Socratic Teaching Approach" above]
"""
```

**Multi-Agent Coordination** (if applicable):
```
Student Query
    ↓
[Primary Tutor] identifies query type
    ↓
If [condition] → handoff to [Secondary Tutor]
    ↓
[Secondary Tutor] continues with context
    ↓
Final response + progress tracking
```

---

### RAG System Integration

**Knowledge Sources Needed**:
1. [Source 1 - e.g., "Python official documentation for loops"]
2. [Source 2 - e.g., "Interactive coding tutorials"]
3. [Source 3 - e.g., "Age-appropriate programming examples"]

**Multi-API Data Collection Strategy**:

| API | Purpose | Query Example | Expected Results |
|-----|---------|---------------|------------------|
| **Tavily** | Breadth - Comprehensive information | "Python loops tutorial for beginners" | 3 results - overview articles |
| **Exa** | Semantics - Conceptually similar content | "how to teach loops to kids" | 3 results - educational resources |
| **Firecrawl** | Depth - Detailed scraping of specific sites | "https://docs.python.org/3/tutorial/controlflow.html" | 5 results - deep content |

**Search Trigger Conditions**:
```python
# When to trigger web research
if semantic_distance > 0.7:  # Insufficient context in ChromaDB
    results = await data_collector.collect_from_all_apis(
        query=enhanced_query,
        max_results=11  # 3 Tavily + 3 Exa + 5 Firecrawl
    )
    # Add to knowledge base with deduplication (MD5 hashing)
    knowledge_base.add_documents(deduplicate(results))
```

**ChromaDB Collection Updates**:
```python
# Collection name: educational_content
# Add new embeddings:
collection.add(
    documents=[content],
    metadatas=[{
        'topic': '[topic_name]',
        'age_group': '[10-16|14-18]',
        'source': '[tavily|exa|firecrawl]',
        'cultural_context': 'mexican',
        'difficulty': '[beginner|intermediate|advanced]'
    }],
    ids=[generate_unique_id()]
)
```

---

### Database Schema Changes

**Neon PostgreSQL (dark-heart-74010500)**

**New Tables** (if any):
```sql
-- Example: New table for feature-specific data
CREATE TABLE feature_name (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    [feature_specific_columns],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Existing Table Modifications**:

**StudentProgress**:
```sql
-- Add new columns for progress tracking
ALTER TABLE student_progress
ADD COLUMN [feature_name]_completed BOOLEAN DEFAULT FALSE,
ADD COLUMN [feature_name]_score INTEGER,
ADD COLUMN [feature_name]_time_spent INTEGER; -- in seconds
```

**LessonContent**:
```sql
-- Add new lessons
INSERT INTO lesson_content (title, category, difficulty, age_group, content_json)
VALUES (
    '[Lesson Title]',
    '[Category]',
    '[beginner|intermediate|advanced]',
    '[10-16|14-18]',
    '{"objectives": [...], "examples": [...], "cultural_refs": [...]}'
);
```

**StudentInteraction**:
```sql
-- Track conversations for this feature
-- No schema change needed - uses existing structure
-- Just ensure proper tagging in interaction_type column
```

**Migration Script**:
```bash
# Create: migrations/[timestamp]_[feature_name].sql
# Apply: psql $DATABASE_URL -f migrations/[timestamp]_[feature_name].sql
```

---

### API Endpoints

**FastAPI Routes** (in `api_server.py`):

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/feature-name", tags=["FeatureName"])

class FeatureRequest(BaseModel):
    student_message: str
    age_group: str  # "10-16" or "14-18"
    tutor_type: str
    context: dict = {}

class FeatureResponse(BaseModel):
    response: str
    progress_update: dict
    suggested_next_steps: list[str]
    cultural_examples_used: list[str]

@router.post("/chat", response_model=FeatureResponse)
async def feature_chat(request: FeatureRequest):
    """
    Handle student interactions for [feature_name].

    Uses Socratic method and age-appropriate cultural examples.
    """
    # Get appropriate tutor
    tutor = get_tutor(request.tutor_type)

    # Generate Socratic response
    response = await tutor.get_response(
        message=request.student_message,
        age_group=request.age_group,
        context=request.context
    )

    # Update progress in Neon database
    progress = await update_student_progress(
        feature="[feature_name]",
        student_id=request.context.get("student_id"),
        interaction_data=response.metadata
    )

    return FeatureResponse(
        response=response.text,
        progress_update=progress,
        suggested_next_steps=response.next_steps,
        cultural_examples_used=response.cultural_refs
    )

@router.get("/progress/{student_id}")
async def get_feature_progress(student_id: int):
    """Get student's progress on this feature."""
    # Query Neon database
    progress = await db.query_student_progress(student_id, "[feature_name]")
    return progress
```

---

### Frontend Components

#### Streamlit Interface (Development)

**File**: `src/ui/app.py`

```python
import streamlit as st
from src.agents.tutor_agent import get_tutor

# Add to sidebar
feature_option = st.sidebar.selectbox(
    "Nueva Función",
    ["[Feature Name]", "Otras opciones..."]
)

if feature_option == "[Feature Name]":
    st.title("📚 [Feature Name]")

    # Age group selector
    age_group = st.selectbox(
        "Selecciona tu edad",
        ["10-16 años", "14-18 años"]
    )

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display conversation
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
    if user_input := st.chat_input("Escribe tu pregunta..."):
        # Get Socratic response
        tutor = get_tutor("programming")  # or appropriate tutor
        response = await tutor.get_response(user_input, age_group)

        # Update UI
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    # Progress visualization
    st.sidebar.metric(
        "Progreso en [Feature Name]",
        f"{progress_percentage}%",
        delta=f"+{recent_gain}%"
    )
```

#### Next.js Interface (Production)

**File**: `frontend/src/components/[FeatureName]/FeatureChat.tsx`

```typescript
'use client';

import { useChat } from 'ai/react';
import { useState } from 'react';
import { motion } from 'framer-motion';

interface FeatureChatProps {
  ageGroup: '10-16' | '14-18';
}

export function FeatureChat({ ageGroup }: FeatureChatProps) {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/feature-name/chat',
    body: {
      age_group: ageGroup,
      tutor_type: 'programming', // or appropriate tutor
    },
  });

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Age-appropriate header */}
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className={ageGroup === '10-16' ? 'text-4xl font-bold text-blue-600' : 'text-3xl font-semibold text-gray-800'}
      >
        {ageGroup === '10-16' ? '🎨 [Feature Name]' : '[Feature Name] - Tutorial Interactivo'}
      </motion.h1>

      {/* Chat messages */}
      <div className="mt-8 space-y-4">
        {messages.map((msg) => (
          <motion.div
            key={msg.id}
            initial={{ opacity: 0, x: msg.role === 'user' ? 20 : -20 }}
            animate={{ opacity: 1, x: 0 }}
            className={`p-4 rounded-lg ${
              msg.role === 'user'
                ? 'bg-blue-100 ml-auto max-w-[80%]'
                : 'bg-gray-100 mr-auto max-w-[80%]'
            }`}
          >
            {msg.content}
          </motion.div>
        ))}
      </div>

      {/* Input form - age-appropriate styling */}
      <form onSubmit={handleSubmit} className="mt-8">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder={
            ageGroup === '10-16'
              ? '¿Qué quieres aprender hoy? 🚀'
              : 'Escribe tu pregunta...'
          }
          className={`w-full p-4 rounded-lg border-2 ${
            ageGroup === '10-16'
              ? 'border-blue-400 text-lg'
              : 'border-gray-300 text-base'
          }`}
          disabled={isLoading}
        />
      </form>

      {/* Progress indicator */}
      <ProgressBar ageGroup={ageGroup} />
    </div>
  );
}
```

**API Route**: `frontend/src/app/api/feature-name/chat/route.ts`

```typescript
import { StreamingTextResponse } from 'ai';

export async function POST(req: Request) {
  const { student_message, age_group, tutor_type, context } = await req.json();

  // Call Python backend
  const response = await fetch(`${process.env.BACKEND_URL}/api/feature-name/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ student_message, age_group, tutor_type, context }),
  });

  // Stream response back to frontend
  return new StreamingTextResponse(response.body);
}
```

---

## Implementation Plan

### Phase 1: Backend Foundation (Days 1-2)

**Tasks**:
- [ ] Update tutor agent system prompts with Socratic patterns
- [ ] Add RAG system enhancements (Tavily + Exa + Firecrawl queries)
- [ ] Create database migration script for schema changes
- [ ] Apply migration to Neon PostgreSQL (dark-heart-74010500)
- [ ] Implement FastAPI endpoints
- [ ] Write unit tests for new tutor logic
- [ ] Test RAG system with sample queries

**Success Criteria**:
- Tutor responds with Socratic questions (not direct answers)
- RAG system returns 11+ sources per query
- Database schema updated successfully
- All unit tests passing

---

### Phase 2: Frontend Integration (Days 3-4)

**Tasks**:
- [ ] Build Streamlit prototype with age-appropriate UI
- [ ] Create Next.js production components
- [ ] Implement progress visualization
- [ ] Add cultural example displays
- [ ] Connect frontend to backend API
- [ ] Test streaming responses (Vercel AI SDK)
- [ ] Implement age-group switching

**Success Criteria**:
- Streamlit dev interface functional
- Next.js production build successful
- UI adapts to age group (10-16 vs 14-18)
- Cultural examples display correctly

---

### Phase 3: Cultural Adaptation (Day 5)

**Tasks**:
- [ ] Review all Mexican cultural examples for accuracy
- [ ] Adjust language complexity for each age group
- [ ] Implement celebratory encouragement patterns
- [ ] Test with age-appropriate sample queries
- [ ] Validate Socratic conversation flows
- [ ] Ensure no direct answers are given

**Success Criteria**:
- Cultural examples reviewed by Mexican educator (if available)
- Vocabulary appropriate for target age
- Socratic method verified in all responses
- Encouragement patterns culturally sensitive

---

### Phase 4: Testing & Validation (Day 6-7)

**Tasks**:
- [ ] Run full `/validate` suite
- [ ] Test multi-agent coordination (if applicable)
- [ ] Validate RAG system deduplication
- [ ] End-to-end user flow testing
- [ ] Performance testing (response latency < 3s)
- [ ] Security review (no API keys hardcoded)
- [ ] Accessibility testing (age-appropriate UI)

**Success Criteria**:
- All 5/5 SDK tests passing
- Integration tests passing
- No performance degradation
- Cultural and age-appropriate content verified

---

### Phase 5: Deployment (Day 8)

**Tasks**:
- [ ] Update CLAUDE.md with new feature
- [ ] Update PLANNING.md with architecture decisions
- [ ] Update TASK.md with completion status
- [ ] Commit code with descriptive message
- [ ] Deploy to Vercel (auto-deploy on push to main)
- [ ] Verify production deployment
- [ ] Monitor for errors in first 24 hours

**Success Criteria**:
- Feature live on https://claude-education-platform-et9fb0qdy-scientia-capital.vercel.app
- Documentation updated
- No production errors
- Git tagged with version number

---

## Success Criteria

### Educational Metrics

1. **Learning Outcome Achievement**: Students demonstrate understanding through discovery (not memorization)
2. **Engagement**: Students ask follow-up questions and explore concepts
3. **Cultural Relevance**: Students relate examples to their own experiences
4. **Age Appropriateness**: Content complexity matches student capability

### Technical Metrics

1. **Response Latency**: < 3 seconds for tutor responses
2. **RAG Quality**: Semantic distance < 0.7 for retrieved context
3. **API Coverage**: 11+ sources per knowledge augmentation (3 Tavily + 3 Exa + 5 Firecrawl)
4. **Test Coverage**: > 80% code coverage
5. **Build Success**: Frontend builds without errors

### User Experience Metrics

1. **Satisfaction**: Positive feedback from students (if user testing available)
2. **Completion Rate**: Students finish lessons/activities
3. **Return Rate**: Students come back for more learning
4. **Progress Tracking**: Student progress accurately recorded in database

---

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Tutor gives direct answers (violates Socratic method) | High | Medium | Comprehensive prompt testing, add examples of what NOT to do |
| Cultural examples not relatable | Medium | Low | Review with Mexican educators, use common cultural touchpoints |
| RAG system returns irrelevant content | Medium | Low | Refine search queries, adjust distance threshold, improve deduplication |
| Age-inappropriate content | High | Low | Strict vocabulary filters, manual content review before deployment |
| API rate limits (Tavily/Exa/Firecrawl) | Medium | Medium | Implement caching, exponential backoff, fallback to ChromaDB only |
| Database migration fails | High | Low | Test migration on dev database first, have rollback script ready |
| Frontend performance issues | Low | Low | Lazy loading, code splitting, optimize bundle size |

---

## Testing Strategy

### Unit Tests

**File**: `tests/test_[feature_name].py`

```python
import pytest
from src.agents.[tutor_name] import [TutorClass]

@pytest.mark.asyncio
async def test_socratic_response_not_direct_answer():
    """Ensure tutor asks guiding questions, not direct answers."""
    tutor = [TutorClass]()
    response = await tutor.get_response("¿Cómo hago un loop?", age_group="10-16")

    # Should NOT contain direct code examples immediately
    assert "for i in range" not in response.lower()
    # Should contain a guiding question
    assert "?" in response

@pytest.mark.asyncio
async def test_cultural_examples_included():
    """Verify Mexican cultural examples are used."""
    tutor = [TutorClass]()
    response = await tutor.get_response("Dame un ejemplo de lista", age_group="10-16")

    # Should use Mexican cultural references
    cultural_keywords = ["taqueria", "tacos", "méxico", "lucha libre"]
    assert any(keyword in response.lower() for keyword in cultural_keywords)

@pytest.mark.asyncio
async def test_age_appropriate_language():
    """Check vocabulary complexity matches age group."""
    tutor = [TutorClass]()

    # Ages 10-16 should use simple language
    response_young = await tutor.get_response("¿Qué es un algoritmo?", age_group="10-16")
    assert "pasos a seguir" in response_young.lower() or "instrucciones" in response_young.lower()

    # Ages 14-18 can use technical terms
    response_older = await tutor.get_response("¿Qué es un algoritmo?", age_group="14-18")
    # Should contain more technical explanation
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_rag_system_enhancement():
    """Verify RAG system augments knowledge when needed."""
    # Simulate query with insufficient local context
    from src.rag.knowledge_base import KnowledgeBase
    from src.tools.data_collector import DataCollector

    kb = KnowledgeBase()
    collector = DataCollector()

    # Search for obscure topic
    results = kb.search("advanced JavaScript closures for beginners")

    # If distance > 0.7, should trigger web research
    if results['distance'] > 0.7:
        web_results = await collector.collect_from_all_apis(
            "JavaScript closures explained for kids"
        )
        assert len(web_results) >= 11  # 3 Tavily + 3 Exa + 5 Firecrawl

@pytest.mark.asyncio
async def test_database_progress_tracking():
    """Ensure student progress is recorded in Neon database."""
    from config.database import get_session
    from config.models import StudentProgress

    session = next(get_session())

    # Simulate feature completion
    progress = StudentProgress(
        student_id=1,
        feature_name_completed=True,
        feature_name_score=85,
        feature_name_time_spent=1200  # 20 minutes
    )
    session.add(progress)
    session.commit()

    # Verify recorded
    retrieved = session.query(StudentProgress).filter_by(student_id=1).first()
    assert retrieved.feature_name_completed is True
    assert retrieved.feature_name_score == 85
```

### User Acceptance Testing

**Test Scenarios**:

1. **Ages 10-16 Student**:
   - Asks simple question about loops
   - Expects colorful UI, simple vocabulary, guiding questions
   - Cultural example should be relatable (e.g., taqueria)
   - Should feel encouraged, not overwhelmed

2. **Ages 14-18 Student**:
   - Asks technical question about async/await
   - Expects more compact UI, technical terms, code examples
   - Still uses Socratic method but allows more depth
   - Progress tracking visible

---

## Deployment Checklist

### Pre-Deployment

- [ ] All unit tests passing (`pytest tests/`)
- [ ] Integration tests passing (`python test_integration.py`)
- [ ] Frontend builds successfully (`npm run build`)
- [ ] NO OpenAI models in code (`grep -r "openai" src/`)
- [ ] API keys only in `.env` files (not hardcoded)
- [ ] Cultural examples reviewed for appropriateness
- [ ] Age-appropriate content validated
- [ ] Socratic method verified (no direct answers)
- [ ] RAG system returning 11+ sources per query
- [ ] Database migration tested on dev database

### Deployment

- [ ] Commit code with descriptive message
- [ ] Tag release with version number
- [ ] Push to GitHub main branch
- [ ] Vercel auto-deploys (verify at deployment URL)
- [ ] Run `/validate` on production
- [ ] Test new feature in production environment

### Post-Deployment

- [ ] Monitor for errors in Vercel dashboard (first 24 hours)
- [ ] Check Neon database for progress tracking data
- [ ] Verify cultural examples display correctly in production
- [ ] Test with both age groups in production
- [ ] Update documentation:
  - [ ] CLAUDE.md (feature added to status)
  - [ ] PLANNING.md (architecture decisions documented)
  - [ ] TASK.md (completion status updated)
  - [ ] README.md (if user-facing changes)

---

## Critical Educational Platform Rules

**ENFORCE THESE ALWAYS:**

1. **NO OpenAI models** - Use Anthropic Claude, Gemini, or Firecrawl only
2. **Age-appropriate content** - Test with both 10-16 and 14-18 age groups
3. **Cultural sensitivity** - Mexican cultural references required, review before deployment
4. **Socratic method** - Guide discovery, never give direct answers
5. **API keys in .env only** - Never hardcode, check before commit
6. **Multi-API data collection** - Use all three: Tavily + Exa + Firecrawl
7. **Dual interface support** - Test both Streamlit (dev) and Next.js (prod)
8. **Progress tracking** - Ensure Neon database records student progress

---

## References

- **Project Documentation**: `/CLAUDE.md`, `/PLANNING.md`, `/TASK.md`
- **Architecture Guide**: `/.claude/architecture.md`
- **Neon Database**: https://console.neon.tech/app/projects/dark-heart-74010500
- **Vercel Deployment**: https://claude-education-platform-et9fb0qdy-scientia-capital.vercel.app
- **GitHub Repository**: [Your repo URL]

---

**Last Updated**: [Date]
**Neon Project**: dark-heart-74010500
**Vercel URL**: https://claude-education-platform-et9fb0qdy-scientia-capital.vercel.app
