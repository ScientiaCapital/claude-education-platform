---
description: "Generate a Project Requirements Plan (PRP) for new features"
---

# Generate PRP - Educational Platform Edition

Create a comprehensive Project Requirements Plan (PRP) for new features in the claude-education-platform.

## Usage

```bash
/generate-prp [feature_name]
```

**Example**:
```bash
/generate-prp advanced-math-tutor
```

---

## What is a PRP?

A **Project Requirements Plan** is a detailed implementation blueprint that includes:
- Educational objectives and learning outcomes
- Technical architecture and API integration points
- Multi-agent tutor coordination patterns
- RAG system enhancements
- Database schema updates
- Frontend UI/UX considerations
- Cultural adaptation requirements
- Testing and validation criteria

---

## PRP Generation Process

### Step 1: Educational Analysis

**Questions to Answer**:
1. What age group is this feature for? (10-16, 14-18, or both?)
2. What learning objectives does this achieve?
3. How does this fit into the Socratic teaching methodology?
4. What Mexican cultural examples can we use?
5. Does this require new curriculum content?

### Step 2: Technical Architecture

**Questions to Answer**:
1. Which tutor agent handles this? (ChatbotTutor, ModelTrainingTutor, ProgrammingTutor, or new?)
2. Does this need RAG enhancement? (web research via Tavily/Exa/Firecrawl?)
3. What database schema changes are required? (StudentProgress, LessonContent, StudentInteraction)
4. Does this need ChromaDB updates? (new vector embeddings, collection updates)
5. What API endpoints are needed? (FastAPI routes for frontend)

### Step 3: Multi-Agent Coordination

**Questions to Answer**:
1. Does this feature require multiple tutors working together?
2. What is the agent handoff flow?
3. How do we maintain conversation context across agents?
4. What prompts need updating for agent coordination?

### Step 4: RAG System Integration

**Questions to Answer**:
1. What knowledge sources are needed? (web, curriculum files, code examples)
2. What search queries should trigger data collection?
3. How do we handle insufficient context? (distance > 0.7 threshold)
4. Which APIs are best suited? (Tavily for breadth, Exa for semantics, Firecrawl for depth)

### Step 5: Frontend Requirements

**Questions to Answer**:
1. Streamlit changes needed? (development interface)
2. Next.js component updates? (production interface)
3. What UI patterns are age-appropriate?
4. How do we visualize progress and learning outcomes?
5. Does this need new animations? (Framer Motion patterns)

### Step 6: Cultural Adaptation

**Questions to Answer**:
1. What Mexican cultural references enhance learning?
2. Are there local examples that make concepts clearer?
3. How do we handle language complexity for different age groups?
4. What celebrations/encouragement patterns fit the culture?

---

## PRP Template Structure

When generating a PRP, use this structure:

```markdown
# PRP: [Feature Name]

## Executive Summary
- **Purpose**: [One sentence learning objective]
- **Target Age**: [10-16, 14-18, or both]
- **Complexity**: [Low/Medium/High]
- **Estimated Effort**: [Small/Medium/Large]

## Educational Objectives
1. [Learning outcome 1]
2. [Learning outcome 2]
3. [Learning outcome 3]

## Cultural Context
- **Mexican Examples**: [List relevant cultural references]
- **Language Complexity**: [Vocabulary level for target age]
- **Encouragement Patterns**: [How we celebrate progress]

## Technical Architecture

### Tutor Agent Changes
- **Affected Tutors**: [Which agents need updates]
- **New Prompts**: [System prompts to add/modify]
- **Coordination Flow**: [Multi-agent handoff diagram]

### RAG System Updates
- **Knowledge Sources**: [What we need to collect]
- **Search Triggers**: [When to trigger web research]
- **API Strategy**: [Tavily/Exa/Firecrawl usage]

### Database Schema
- **New Tables**: [If any]
- **Schema Modifications**: [Existing table updates]
- **Migration Script**: [SQL changes needed]

### API Endpoints
```python
# New FastAPI routes needed
@app.post("/api/feature-name")
async def feature_endpoint(...):
    pass
```

### Frontend Components
- **Streamlit**: [Development interface changes]
- **Next.js**: [Production interface changes]
- **UI Patterns**: [Age-appropriate design decisions]

## Implementation Plan

### Phase 1: Backend Foundation
- [ ] Update tutor agent prompts
- [ ] Add RAG system enhancements
- [ ] Database schema migration
- [ ] API endpoint implementation

### Phase 2: Frontend Integration
- [ ] Streamlit prototype
- [ ] Next.js production component
- [ ] Progress visualization
- [ ] Testing with age-appropriate scenarios

### Phase 3: Cultural Adaptation
- [ ] Add Mexican cultural examples
- [ ] Adjust language complexity
- [ ] Implement encouragement patterns
- [ ] User testing with target age group

### Phase 4: Testing & Validation
- [ ] Unit tests for new code
- [ ] Integration tests for multi-agent flow
- [ ] RAG system validation
- [ ] Age-appropriate content review

## Success Criteria
1. [Measurable learning outcome]
2. [Technical performance metric]
3. [User engagement metric]
4. [Cultural appropriateness validation]

## Risks & Mitigation
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | [High/Med/Low] | [Strategy] |

## Testing Strategy
- **Unit Tests**: [What to test]
- **Integration Tests**: [Flow to validate]
- **User Testing**: [Age group scenarios]

## Deployment Checklist
- [ ] Backend tests passing (pytest)
- [ ] Frontend builds successfully
- [ ] Vercel deployment updated
- [ ] Neon database migrated
- [ ] ChromaDB vectors updated
- [ ] API documentation updated
```

---

## Educational Platform Patterns to Include

### Pattern 1: Socratic Teaching Flow
```python
# Always guide with questions, not answers
async def socratic_response(student_query: str) -> str:
    # 1. Understand what student knows
    # 2. Ask probing question
    # 3. Wait for student to discover answer
    # 4. Provide gentle guidance if stuck
    # 5. Celebrate discovery
```

### Pattern 2: Multi-API RAG Enhancement
```python
# Use all three APIs for comprehensive context
async def enhance_context(query: str) -> List[Document]:
    tavily_results = await data_collector.search_tavily(query)  # Breadth
    exa_results = await data_collector.search_exa(query)        # Semantics
    firecrawl_results = await data_collector.scrape_firecrawl(url)  # Depth
    return deduplicate_and_rank(tavily_results + exa_results + firecrawl_results)
```

### Pattern 3: Age-Appropriate Content Adaptation
```python
# Adjust complexity based on age group
def adapt_for_age(content: str, age_group: str) -> str:
    if age_group == "10-16":
        return simplify_vocabulary(content, add_visual_examples=True)
    elif age_group == "14-18":
        return add_technical_depth(content, include_code_samples=True)
```

### Pattern 4: Dual Interface (Streamlit + Next.js)
```python
# Backend API serves both interfaces
@app.post("/api/tutor/chat")
async def chat_endpoint(message: str, tutor_type: str):
    tutor = get_tutor(tutor_type)
    response = await tutor.get_response(message)
    return {"response": response, "progress": calculate_progress()}
```

---

## Critical Rules for PRPs

**MUST ENFORCE:**

1. **NO OpenAI models** - Use Anthropic Claude, Gemini, or Firecrawl only
2. **Age-appropriate content** - Separate strategies for 10-16 and 14-18
3. **Cultural sensitivity** - Mexican cultural references required
4. **Socratic method** - Guide discovery, don't give direct answers
5. **API keys in .env only** - Never hardcode credentials
6. **Multi-API data collection** - Use all three: Tavily + Exa + Firecrawl
7. **Dual interface support** - Both Streamlit (dev) and Next.js (prod)

---

## After PRP Generation

1. **Save to**: `PRPs/[feature_name]_PRP.md`
2. **Review with**: `/execute-prp [feature_name]`
3. **Track in**: `PLANNING.md` (update architecture decisions)
4. **Test with**: `/validate` (full system validation)

---

## Example PRP Generation Session

**User Request**: "I want to add a JavaScript tutorial to the programming tutor"

**Claude Response**:
```
I'll generate a comprehensive PRP for adding JavaScript tutorials. Let me analyze:

Educational Objectives:
- Target: Ages 14-18 (JavaScript is appropriate for older students)
- Learning outcome: Students can write basic JS functions and understand DOM manipulation
- Mexican cultural examples: Build a "Taqueria order system" web app

Technical Architecture:
- Agent: ProgrammingTutor (update system prompts)
- RAG: Collect MDN docs, JavaScript.info, and Mexican coding blogs
- Database: Add JavaScript lessons to LessonContent table
- Frontend: Interactive code editor with live preview

Multi-API Strategy:
- Tavily: General JavaScript tutorials
- Exa: Semantic search for "interactive JavaScript learning"
- Firecrawl: Deep scrape MDN and JavaScript.info

Creating PRP: PRPs/javascript_tutorial_PRP.md...
```

---

**Last Updated**: 2025-11-30
**Neon Project**: dark-heart-74010500
**Vercel URL**: https://claude-education-platform-et9fb0qdy-scientia-capital.vercel.app
