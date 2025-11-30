# PLANNING.md - Claude Education Platform

**Project**: Multi-Agent Educational System for Mexican Students
**Tech Stack**: Python + FastAPI + Streamlit + Next.js + Supabase/Neon PostgreSQL + ChromaDB
**Target**: Mexican students ages 10-18
**Methodology**: Socratic teaching with cultural adaptation

---

## Architecture Overview

### System Flow: Student Learning Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                    STUDENT QUERY                                │
│              ("¿Cómo funciona un loop?")                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   TUTOR AGENT ROUTER                            │
│   Determines which tutor to use based on query                  │
│   - ChatbotTutor (chatbot creation)                            │
│   - ModelTrainingTutor (ML concepts)                           │
│   - ProgrammingTutor (coding concepts)                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 KNOWLEDGE BASE SEARCH                           │
│   ChromaDB vector search for relevant context                  │
│   - Searches existing curriculum content                       │
│   - Calculates semantic distance                               │
│   - Returns most relevant documents (if distance < 0.7)        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
                  ┌──────┴──────┐
                  │             │
         Distance < 0.7?   Distance > 0.7?
         (Sufficient)      (Insufficient)
                  │             │
                  │             ▼
                  │   ┌──────────────────────────────────────┐
                  │   │   RAG ENHANCEMENT                    │
                  │   │   Trigger multi-API data collection: │
                  │   │   - Tavily (3 results - breadth)    │
                  │   │   - Exa (3 results - semantics)     │
                  │   │   - Firecrawl (5 results - depth)   │
                  │   │   Total: 11 sources per query        │
                  │   └──────────┬───────────────────────────┘
                  │              │
                  │              ▼
                  │   ┌──────────────────────────────────────┐
                  │   │   KNOWLEDGE BASE UPDATE              │
                  │   │   - Deduplicate (MD5 hashing)       │
                  │   │   - Add to ChromaDB                 │
                  │   │   - Update metadata                 │
                  │   └──────────┬───────────────────────────┘
                  │              │
                  └──────┬───────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│               SOCRATIC RESPONSE GENERATION                      │
│   Tutor generates age-appropriate response using:              │
│   - Retrieved context (local + web if augmented)               │
│   - Mexican cultural examples                                  │
│   - Socratic questioning methodology                           │
│   - Age-appropriate language (10-16 vs 14-18)                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  PROGRESS TRACKING                              │
│   Update Neon PostgreSQL:                                       │
│   - StudentProgress (completion, scores, time)                 │
│   - StudentInteraction (conversation history)                  │
│   - LessonContent (if new content added)                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│               STUDENT RESPONSE + UI UPDATE                      │
│   Return to frontend:                                           │
│   - Socratic guiding question (not direct answer)              │
│   - Cultural examples visualization                            │
│   - Progress metrics                                            │
│   - Suggested next steps                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Three Specialized Tutors Design

### Design Decision: Domain-Specific Tutors

**Rationale**: Specialized tutors provide deeper domain expertise and more relevant Socratic questioning patterns than a single generalist tutor.

**Architecture**:

```
┌────────────────────────────────────────────────────────────────┐
│               EducationalTutor (Base Class)                    │
│                                                                │
│  Core Capabilities:                                            │
│  - Socratic method implementation                             │
│  - Age-appropriate language adaptation                        │
│  - Mexican cultural context integration                       │
│  - RAG system interaction                                     │
│  - Progress tracking                                           │
└────────────────────────┬───────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌─────────────┐  ┌──────────────┐  ┌────────────────┐
│ ChatbotTutor│  │ModelTraining │  │Programming     │
│             │  │Tutor         │  │Tutor           │
└─────────────┘  └──────────────┘  └────────────────┘

Specialization 1:    Specialization 2:    Specialization 3:
Chatbot Creation     ML Concepts          Coding Concepts
```

### ChatbotTutor

**Domain**: Natural language processing, chatbot design, conversation flows

**Specialized Prompts**:
- "¿Qué tipo de preguntas quieres que tu chatbot responda?"
- "Piensa en una conversación con un amigo. ¿Cómo fluye naturalmente?"
- "¿Qué pasaría si tu chatbot no entiende una pregunta?"

**Cultural Examples**:
- "Imagina un chatbot para una taqueria que toma pedidos..."
- "¿Cómo respondería un chatbot si alguien pregunta por quesadillas vs tacos?"

**Age Adaptations**:
- **10-16**: Focus on simple question-answer patterns, visual flowcharts
- **14-18**: Introduce NLP concepts, intent recognition, context management

---

### ModelTrainingTutor

**Domain**: Machine learning concepts, model training, data preparation

**Specialized Prompts**:
- "¿Cómo le enseñarías a una computadora a reconocer un taco de un burrito?"
- "¿Qué ejemplos necesitaría ver la computadora para aprender?"
- "Si tu modelo comete errores, ¿qué podría estar aprendiendo mal?"

**Cultural Examples**:
- "Entrenemos un modelo para clasificar tipos de tacos (pastor, carnitas, suadero)..."
- "¿Qué características distinguen una quesadilla de un taco?"
- "Predicción de ventas para un puesto de tacos basado en clima y día de la semana"

**Age Adaptations**:
- **10-16**: Use visual analogies (teaching vs learning), avoid math
- **14-18**: Introduce technical concepts (features, labels, accuracy) with code

---

### ProgrammingTutor

**Domain**: Programming fundamentals, algorithms, data structures

**Specialized Prompts**:
- "¿Qué pasos seguirías si tuvieras que ordenar una lista de tacos por precio?"
- "¿Cómo le explicarías a alguien que repita una tarea 10 veces?"
- "Si tu programa tiene un error, ¿cómo encontrarías dónde está?"

**Cultural Examples**:
- "Crea un programa para gestionar inventario de una taqueria..."
- "Algoritmo de ordenamiento usando luchadores de lucha libre por peso"
- "Sistema de calendario para celebraciones de Día de los Muertos"

**Age Adaptations**:
- **10-16**: Visual programming concepts, block-based thinking
- **14-18**: Real code examples, debugging strategies, best practices

---

## Database Schema (Neon PostgreSQL)

### Design Decision: Dual Database Strategy

**Rationale**:
- **ChromaDB**: Optimized for vector similarity search (RAG system)
- **Neon PostgreSQL**: Relational data, ACID compliance, serverless scalability

**Neon Project**: `dark-heart-74010500`

### Schema Tables

#### 1. StudentProgress

**Purpose**: Track student learning progress across all features

```sql
CREATE TABLE student_progress (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    topic VARCHAR(100) NOT NULL,  -- e.g., "python_loops", "chatbot_basics"

    -- Completion tracking
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    is_completed BOOLEAN DEFAULT FALSE,

    -- Performance metrics
    score INTEGER CHECK (score >= 0 AND score <= 100),
    time_spent_seconds INTEGER DEFAULT 0,
    attempts INTEGER DEFAULT 1,

    -- Learning journey
    lessons_completed INTEGER DEFAULT 0,
    exercises_completed INTEGER DEFAULT 0,
    challenges_completed INTEGER DEFAULT 0,

    -- Metadata
    age_group VARCHAR(10) CHECK (age_group IN ('10-16', '14-18')),
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(student_id, topic)
);

-- Indexes for common queries
CREATE INDEX idx_student_progress_student ON student_progress(student_id);
CREATE INDEX idx_student_progress_topic ON student_progress(topic);
CREATE INDEX idx_student_progress_completed ON student_progress(is_completed);
```

#### 2. LessonContent

**Purpose**: Structured curriculum with cultural adaptations

```sql
CREATE TABLE lesson_content (
    id SERIAL PRIMARY KEY,

    -- Lesson identification
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL,  -- 'chatbot', 'ml', 'programming'

    -- Content targeting
    age_group VARCHAR(10) CHECK (age_group IN ('10-16', '14-18', 'both')),
    difficulty VARCHAR(20) CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),

    -- Content structure (JSON)
    content_json JSONB NOT NULL,
    /*
    Example structure:
    {
      "objectives": ["Learn loops", "Understand iteration"],
      "cultural_examples": [
        {
          "title": "Taqueria Inventory",
          "description": "Usa loops para contar ingredientes...",
          "code_example": "for taco in tacos: print(taco)"
        }
      ],
      "socratic_prompts": [
        "¿Qué pasaría si...?",
        "¿Cómo podrías...?"
      ],
      "activities": [
        {
          "type": "hands-on",
          "duration_minutes": 15,
          "instructions": "..."
        }
      ]
    }
    */

    -- Metadata
    estimated_duration_minutes INTEGER,
    prerequisites JSONB DEFAULT '[]',  -- List of prerequisite lesson slugs
    tags JSONB DEFAULT '[]',  -- ['loops', 'python', 'beginner']

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Indexes
CREATE INDEX idx_lesson_category ON lesson_content(category);
CREATE INDEX idx_lesson_age_group ON lesson_content(age_group);
CREATE INDEX idx_lesson_difficulty ON lesson_content(difficulty);
CREATE INDEX idx_lesson_tags ON lesson_content USING GIN(tags);
```

#### 3. StudentInteraction

**Purpose**: Conversation history with satisfaction ratings

```sql
CREATE TABLE student_interaction (
    id SERIAL PRIMARY KEY,

    -- Interaction identification
    student_id INTEGER NOT NULL,
    session_id UUID NOT NULL,
    interaction_type VARCHAR(50) NOT NULL,  -- 'chat', 'exercise', 'challenge'

    -- Conversation data
    tutor_type VARCHAR(50) NOT NULL,  -- 'chatbot', 'model_training', 'programming'
    student_message TEXT NOT NULL,
    tutor_response TEXT NOT NULL,

    -- Context
    age_group VARCHAR(10) CHECK (age_group IN ('10-16', '14-18')),
    lesson_slug VARCHAR(100),  -- References lesson_content.slug

    -- Response metadata (JSON)
    response_metadata JSONB,
    /*
    {
      "cultural_examples_used": ["taqueria", "lucha_libre"],
      "socratic_questions_asked": 3,
      "direct_answers_given": 0,
      "rag_sources_used": ["tavily", "exa"],
      "web_research_triggered": true,
      "semantic_distance": 0.42
    }
    */

    -- Student feedback
    satisfaction_rating INTEGER CHECK (satisfaction_rating >= 1 AND satisfaction_rating <= 5),
    feedback_text TEXT,

    -- Performance tracking
    response_time_ms INTEGER,  -- How long tutor took to respond
    tokens_used INTEGER,

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_interaction_student ON student_interaction(student_id);
CREATE INDEX idx_interaction_session ON student_interaction(session_id);
CREATE INDEX idx_interaction_tutor ON student_interaction(tutor_type);
CREATE INDEX idx_interaction_created ON student_interaction(created_at DESC);
```

---

## Multi-API Data Collection Strategy

### Design Decision: Complementary API Usage

**Rationale**: Each API has unique strengths. Using all three provides:
- **Breadth** (Tavily): Wide range of educational content
- **Semantics** (Exa): Conceptually similar resources
- **Depth** (Firecrawl): Deep scraping of authoritative sources

**Implementation**: `src/tools/data_collector.py`

```python
class DataCollector:
    async def collect_from_all_apis(self, query: str, max_results: int = 11):
        """
        Collect from all three APIs in parallel for comprehensive context.

        Returns:
            List[Document]: Combined results from all APIs
        """
        # Parallel execution for speed
        tavily_task = self.search_tavily(query, max_results=3)
        exa_task = self.search_exa(query, max_results=3)
        firecrawl_task = self.scrape_firecrawl_batch(
            self.get_authoritative_urls(query), max_results=5
        )

        tavily_results, exa_results, firecrawl_results = await asyncio.gather(
            tavily_task, exa_task, firecrawl_task
        )

        # Combine and deduplicate
        all_results = tavily_results + exa_results + firecrawl_results
        return self.deduplicate(all_results)  # MD5 hashing

    def deduplicate(self, documents: List[Document]) -> List[Document]:
        """Remove duplicate content using MD5 hashing."""
        seen_hashes = set()
        unique_docs = []

        for doc in documents:
            content_hash = hashlib.md5(doc.content.encode()).hexdigest()
            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                unique_docs.append(doc)

        return unique_docs
```

### API Usage Patterns

| API | Use Case | Max Results | Strengths | Limitations |
|-----|----------|-------------|-----------|-------------|
| **Tavily** | General educational content discovery | 3 | Fast, diverse sources, good summaries | Can be surface-level |
| **Exa** | Semantically similar learning resources | 3 | Neural search, finds conceptually related content | Requires good query phrasing |
| **Firecrawl** | Deep scraping of documentation sites | 5 | Detailed content, respects robots.txt | Slower, requires target URLs |

**Total per query**: 11 sources (subject to deduplication)

---

## Dual Interface Strategy

### Design Decision: Streamlit (Dev) + Next.js (Prod)

**Rationale**:
- **Streamlit**: Rapid prototyping, easy progress visualization, Python-native
- **Next.js**: Production-ready, optimized performance, better mobile experience

### Architecture

```
┌────────────────────────────────────────────────────────────┐
│                  FastAPI Backend                           │
│                  (api_server.py)                           │
│                                                            │
│  Exposes Python tutor agents as REST endpoints:           │
│  - POST /api/tutor/chat                                   │
│  - GET  /api/student/progress/{id}                        │
│  - POST /api/lesson/complete                              │
└──────────────┬─────────────────────┬───────────────────────┘
               │                     │
               │                     │
       ┌───────▼────────┐    ┌──────▼──────────┐
       │   Streamlit    │    │    Next.js      │
       │   (Dev UI)     │    │   (Prod UI)     │
       │                │    │                 │
       │  src/ui/app.py │    │  frontend/      │
       │                │    │                 │
       │  - Rapid proto │    │  - Production   │
       │  - Progress viz│    │  - SSR          │
       │  - Testing     │    │  - Vercel AI    │
       └────────────────┘    └─────────────────┘
```

### Streamlit Interface (Development)

**File**: `src/ui/app.py`

**Strengths**:
- Instant feedback during development
- Built-in progress charts and metrics
- Easy to add new experimental features
- Python developers can contribute to UI

**Usage**:
```bash
streamlit run src/ui/app.py
```

**Key Components**:
- Sidebar for tutor selection and age group
- Chat interface with conversation history
- Progress visualization (charts, metrics)
- Cultural example displays
- Debugging information (for developers)

---

### Next.js Interface (Production)

**Path**: `frontend/`

**Strengths**:
- Optimized bundle size and performance
- Server-Side Rendering for SEO
- Mobile-responsive by default
- Vercel AI SDK for streaming responses
- Better user experience for end users

**Deployment**:
```bash
cd frontend
npm run build
vercel --prod
```

**Key Components**:
- `src/components/TutorChat.tsx` - Chat interface with streaming
- `src/components/ProgressDashboard.tsx` - Student progress visualization
- `src/app/api/tutor/chat/route.ts` - API route proxying to Python backend
- `src/lib/hooks/useChat.ts` - Vercel AI SDK integration

**API Bridge**:
```typescript
// frontend/src/app/api/tutor/chat/route.ts
export async function POST(req: Request) {
  const { message, tutorType, ageGroup } = await req.json();

  // Call Python backend
  const response = await fetch(`${process.env.BACKEND_URL}/api/tutor/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, tutor_type: tutorType, age_group: ageGroup }),
  });

  // Stream response back to frontend
  return new StreamingTextResponse(response.body);
}
```

---

## Critical Architecture Decisions

### 1. Socratic Method Implementation

**Decision**: Never give direct answers, always guide with questions

**Enforcement**:
- System prompts explicitly forbid direct answers
- Unit tests validate responses contain questions
- Examples in prompts show Socratic patterns

**Example Pattern**:
```python
# In tutor system prompt:
"""
CRITICAL: You MUST use the Socratic method.

✅ GOOD:
Student: "¿Cómo hago un loop?"
You: "¿Qué quieres repetir? ¿Has visto cómo repetimos cosas en la vida diaria?"

❌ BAD (NEVER DO THIS):
Student: "¿Cómo hago un loop?"
You: "Usa 'for i in range(10):' para hacer un loop."
"""
```

---

### 2. Age-Appropriate Content Adaptation

**Decision**: Separate strategies for 10-16 and 14-18 age groups

**Implementation**:
```python
def adapt_for_age(content: str, age_group: str) -> str:
    if age_group == "10-16":
        return simplify_vocabulary(
            content,
            max_sentence_length=15,
            add_visual_examples=True,
            use_colorful_language=True
        )
    elif age_group == "14-18":
        return add_technical_depth(
            content,
            include_code_samples=True,
            explain_terminology=True,
            reference_documentation=True
        )
```

**Vocabulary Guidelines**:

| Concept | Ages 10-16 | Ages 14-18 |
|---------|-----------|-----------|
| Algorithm | "pasos a seguir" | "algoritmo" (with explanation) |
| Function | "instrucción que puedes reutilizar" | "función" (with parameters) |
| Loop | "repetir acciones" | "iteración con for/while" |
| Variable | "una cajita que guarda información" | "variable con tipo de dato" |

---

### 3. Cultural Context Integration

**Decision**: Mandatory Mexican cultural examples in all lessons

**Cultural Touchpoints**:
- **Food**: Tacos, quesadillas, tamales (universal in Mexico)
- **Sports**: Lucha libre, fútbol
- **Celebrations**: Día de los Muertos, Día de la Independencia
- **Geography**: Mexican cities, landmarks
- **Brands**: Mexican companies and products

**Implementation**:
```python
CULTURAL_EXAMPLES = {
    "lists": [
        "ingredientes para tacos (tortilla, carne, cilantro, cebolla)",
        "luchadores de lucha libre ordenados por peso",
        "ciudades de México por población"
    ],
    "sorting": [
        "ordenar tacos por precio",
        "clasificar equipos de fútbol por victorias",
        "organizar ofrendas por fecha"
    ],
    "conditionals": [
        "si hace calor, vender más agua fresca",
        "si es fin de semana, más clientes en la taqueria",
        "si es Día de los Muertos, preparar pan de muerto"
    ]
}
```

---

### 4. RAG System Distance Threshold

**Decision**: Trigger web research when semantic distance > 0.7

**Rationale**:
- Distance < 0.7 = Strong semantic similarity, local context sufficient
- Distance > 0.7 = Weak similarity, likely need fresh information

**Implementation**:
```python
async def get_response(self, student_message: str):
    # Search local knowledge base
    results = self.knowledge_base.search(student_message)

    if results['distance'] > 0.7:
        # Insufficient context, trigger web research
        web_results = await self.data_collector.collect_from_all_apis(
            query=student_message
        )

        # Add to knowledge base
        self.knowledge_base.add_documents(web_results)

        # Re-search with augmented context
        results = self.knowledge_base.search(student_message)

    # Generate Socratic response with context
    return self.generate_socratic_response(student_message, results['documents'])
```

---

### 5. NO OpenAI Models

**Decision**: Use Anthropic Claude, Google Gemini, or Firecrawl only

**Rationale**: Project requirement (see CLAUDE.md)

**Enforcement**:
```python
# In config/settings.py
class Settings(BaseSettings):
    anthropic_api_key: str
    google_api_key: Optional[str] = None  # For Gemini
    firecrawl_api_key: str

    # EXPLICITLY NOT INCLUDED:
    # openai_api_key  ❌ DO NOT ADD

# CI/CD check:
# grep -r "openai" src/ && exit 1  # Fail if OpenAI found
```

---

## Performance Considerations

### Response Latency Targets

| Component | Target | Actual |
|-----------|--------|--------|
| Knowledge base search | < 100ms | ~50ms |
| RAG web research | < 2s | ~1.5s |
| Claude API call | < 2s | ~1.2s |
| **Total tutor response** | **< 3s** | **~2.7s** |

### Database Query Optimization

**Neon PostgreSQL** (serverless, cold start ~200ms):
- Use connection pooling
- Index all foreign keys
- Paginate large result sets
- Cache frequent queries (Redis if needed)

**ChromaDB** (local, fast):
- Pre-compute embeddings
- Use batch operations
- Limit collection size (archive old content)

---

## Security Considerations

### API Keys Management

**Storage**: `.env` files only (never commit)

```env
# Backend .env
ANTHROPIC_API_KEY=sk-ant-...
FIRECRAWL_API_KEY=fc-...
DATABASE_URL=postgresql://...
EXA_API_KEY=...
TAVILY_API_KEY=...

# Frontend .env
NEXT_PUBLIC_BACKEND_URL=https://api.example.com
```

**Validation** (startup check):
```python
# In api_server.py
@app.on_event("startup")
async def validate_environment():
    required_keys = [
        "ANTHROPIC_API_KEY",
        "FIRECRAWL_API_KEY",
        "DATABASE_URL"
    ]
    missing = [key for key in required_keys if not os.getenv(key)]
    if missing:
        raise ValueError(f"Missing required environment variables: {missing}")
```

---

### Student Data Privacy

**Principles**:
- Minimal data collection (only for learning progress)
- No PII in logs or error messages
- Secure database connection (SSL/TLS)
- GDPR-compliant data retention policies

**Implementation**:
```python
# Anonymize student IDs in logs
logger.info(f"Student {hash_student_id(student_id)} completed lesson")

# Don't log student messages
logger.debug("Received student message")  # Not: f"Message: {message}"
```

---

## Testing Strategy

### Unit Tests

**Location**: `tests/`

**Coverage Target**: > 80%

**Key Test Cases**:
- Tutor agents enforce Socratic method
- Age-appropriate language adaptation
- Cultural examples included in responses
- RAG system triggers at correct distance threshold
- Database operations (CRUD)

---

### Integration Tests

**File**: `test_integration.py`

**Scenarios**:
- End-to-end student learning journey
- Multi-agent coordination
- RAG system with web research
- Database progress tracking

---

### SDK Tests

**File**: `test_sdks.py`

**Status**: ✅ 5/5 passing

**Validation**:
1. Environment variables configured
2. Claude SDK integration
3. Firecrawl SDK v2 integration
4. Database model initialization
5. Tutor agent instantiation

---

## Deployment Architecture

### Production Stack

```
┌─────────────────────────────────────────────────────────┐
│                  Vercel (Frontend)                      │
│  https://claude-education-platform-et9fb0qdy-           │
│  scientia-capital.vercel.app                            │
│                                                         │
│  - Next.js SSR                                          │
│  - Edge functions for API routes                       │
│  - Auto-deploy on git push                             │
└────────────┬────────────────────────────────────────────┘
             │
             │ HTTPS
             ▼
┌─────────────────────────────────────────────────────────┐
│            FastAPI Backend (to be deployed)             │
│                                                         │
│  Options:                                               │
│  - Railway.app (recommended)                            │
│  - Render.com                                           │
│  - Fly.io                                               │
└────────────┬────────────────────────────────────────────┘
             │
             │ Pooled connection
             ▼
┌─────────────────────────────────────────────────────────┐
│         Neon PostgreSQL (Serverless)                    │
│         Project: dark-heart-74010500                    │
│                                                         │
│  - Automatic scaling                                    │
│  - Branch databases for dev/staging                     │
│  - Point-in-time recovery                              │
└─────────────────────────────────────────────────────────┘
```

---

## Future Architecture Enhancements

### Planned Improvements

1. **Redis Caching**:
   - Cache frequent knowledge base queries
   - Session management
   - Rate limiting

2. **Webhook Integrations**:
   - Notify parents of student progress
   - Weekly learning summaries
   - Achievement celebrations

3. **Advanced RAG**:
   - Multi-turn conversation context
   - Long-term memory for students
   - Personalized learning paths

4. **Analytics Dashboard**:
   - Aggregate student progress metrics
   - Popular topics and pain points
   - Tutor effectiveness analysis

5. **Mobile App**:
   - React Native or Flutter
   - Offline mode with local ChromaDB
   - Push notifications for lessons

---

**Last Updated**: 2025-11-30
**Neon Project**: dark-heart-74010500
**Vercel URL**: https://claude-education-platform-et9fb0qdy-scientia-capital.vercel.app
**GitHub**: [Repository URL]
