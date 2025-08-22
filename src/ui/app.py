import streamlit as st
import asyncio
from src.agents.tutor_agent import ChatbotTutor, ModelTrainingTutor, ProgrammingTutor
from src.rag.database import db_manager
import plotly.express as px
import pandas as pd
import uuid

# Configure page
st.set_page_config(
    page_title="Claude Education Platform",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "current_tutor" not in st.session_state:
    st.session_state.current_tutor = None
if "student_id" not in st.session_state:
    st.session_state.student_id = str(uuid.uuid4())

# Initialize database tables
@st.cache_resource
def init_database():
    """Initialize database tables on first run"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(db_manager.create_tables())
        return True
    except Exception as e:
        st.error(f"Database initialization error: {e}")
        return False

# Call initialization
init_database()

# Sidebar for tutor selection
st.sidebar.title("🎓 Elige tu Tutor")
tutor_type = st.sidebar.selectbox(
    "¿Qué quieres aprender?",
    ["Crear Chatbots", "Entrenar Modelos IA", "Programación y IA"]
)

# Initialize tutor based on selection
tutor_map = {
    "Crear Chatbots": ChatbotTutor(),
    "Entrenar Modelos IA": ModelTrainingTutor(),
    "Programación y IA": ProgrammingTutor()
}

if st.session_state.current_tutor != tutor_type:
    st.session_state.current_tutor = tutor_type
    st.session_state.conversation_history = []

tutor = tutor_map[tutor_type]

# Main interface
st.title(f"🤖 Tutor de {tutor_type}")
st.markdown("¡Hola! Soy tu tutor de IA. ¿Qué te gustaría aprender hoy?")

# Topic input
topic = st.text_input(
    "Tema o pregunta:",
    placeholder="Por ejemplo: ¿Cómo crear mi primer chatbot?"
)

# Difficulty level selector
difficulty = st.selectbox(
    "Nivel de dificultad:",
    ["Principiante", "Intermedio", "Avanzado"]
)

# Generate lesson button
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🚀 ¡Aprende!", type="primary") and topic:
        with st.spinner("Preparando tu lección personalizada..."):
            try:
                # Run async function
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    tutor.teach_topic(
                        topic=topic, 
                        student_question=topic,
                        student_id=st.session_state.student_id
                    )
                )
                
                # Display results
                st.markdown("## 📚 Tu Lección")
                st.markdown(result["answer"])
                
                # Activities section
                if result["activities"]:
                    st.markdown("## 🎯 Actividades Prácticas")
                    for i, activity in enumerate(result["activities"], 1):
                        if activity.strip():
                            with st.expander(f"Actividad {i}"):
                                st.markdown(activity)
                
                # Sources
                if result["sources"]:
                    with st.expander("📖 Fuentes de información"):
                        for source in result["sources"]:
                            st.markdown(f"- **{source.get('title', 'Sin título')}** ({source.get('source', 'N/A')})")
                
                # Add to conversation history
                st.session_state.conversation_history.append({
                    "topic": topic,
                    "result": result,
                    "difficulty": difficulty,
                    "tutor_type": tutor_type
                })
                
                # Record progress (simple completion for now)
                loop.run_until_complete(
                    tutor.record_progress(
                        student_id=st.session_state.student_id,
                        topic=topic,
                        completion_score=1.0,  # Full completion for viewing lesson
                        time_spent=5  # Estimated 5 minutes per lesson
                    )
                )
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.error("Asegúrate de que las variables de entorno estén configuradas correctamente.")

with col2:
    if st.button("📊 Ver mi progreso"):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            progress = loop.run_until_complete(
                tutor.get_student_history(st.session_state.student_id)
            )
            if progress:
                df = pd.DataFrame([{
                    "Tema": p.topic,
                    "Puntuación": p.completion_score,
                    "Tiempo (min)": p.time_spent,
                    "Fecha": p.created_at.strftime("%Y-%m-%d")
                } for p in progress])
                
                st.markdown("### 📈 Tu Progreso de Aprendizaje")
                st.dataframe(df)
                
                # Progress chart
                fig = px.line(df, x="Fecha", y="Puntuación", 
                             title="Progreso a lo largo del tiempo",
                             markers=True)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("¡Comienza tu primera lección para ver tu progreso!")
        except Exception as e:
            st.error(f"Error al cargar el progreso: {e}")

# Conversation history
if st.session_state.conversation_history:
    st.sidebar.markdown("## 📝 Historial")
    for i, conv in enumerate(st.session_state.conversation_history[-5:]):
        if st.sidebar.button(f"📌 {conv['topic'][:30]}...", key=f"history_{i}"):
            st.markdown(f"### Tema anterior: {conv['topic']}")
            st.markdown(conv['result']['answer'])

# Learning progress visualization
if len(st.session_state.conversation_history) > 1:
    st.sidebar.markdown("## 📊 Sesión Actual")
    
    topics_df = pd.DataFrame([
        {
            "Tema": conv["topic"][:20] + "...", 
            "Orden": i+1,
            "Tutor": conv["tutor_type"]
        } 
        for i, conv in enumerate(st.session_state.conversation_history)
    ])
    
    fig = px.bar(topics_df, x="Orden", y=topics_df.index, 
                 color="Tutor", title="Temas Explorados",
                 orientation='h')
    st.sidebar.plotly_chart(fig, use_container_width=True)

# Footer with instructions
st.markdown("---")
st.markdown("""
### 🚀 Cómo empezar:
1. **Configura tus API keys**: Copia `.env.example` a `.env` y agrega tus claves
2. **Selecciona un tutor** especializado en el área que te interesa
3. **Haz una pregunta** o pide que te enseñe sobre un tema específico
4. **Realiza las actividades** para reforzar tu aprendizaje
5. **Revisa tu progreso** para ver tu evolución

### 🔧 APIs requeridas:
- Anthropic (Claude)
- Firecrawl
- Exa
- Tavily
- Neon Database
""")

# Student ID display (for debugging)
if st.sidebar.checkbox("Mostrar ID de estudiante"):
    st.sidebar.text(f"ID: {st.session_state.student_id}")

# Reset session button
if st.sidebar.button("🔄 Nueva sesión"):
    st.session_state.student_id = str(uuid.uuid4())
    st.session_state.conversation_history = []
    st.rerun()