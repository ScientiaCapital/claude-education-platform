import asyncio
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.agents.tutor_agent import ChatbotTutor, ModelTrainingTutor, ProgrammingTutor
from src.tools.data_collector import DataCollector
from src.rag.knowledge_base import KnowledgeBase

async def demo_chatbot_tutor():
    """Demonstrate the ChatbotTutor functionality"""
    print("🤖 Inicializando Tutor de Chatbots...")
    tutor = ChatbotTutor()
    
    # Teach a topic
    result = await tutor.teach_topic(
        topic="crear chatbot con Python",
        student_question="¿Cómo empiezo mi primer chatbot?"
    )
    
    print("\n🎓 LECCIÓN:")
    print("=" * 50)
    print(result["answer"])
    
    print("\n🎯 ACTIVIDADES PRÁCTICAS:")
    print("=" * 50)
    for i, activity in enumerate(result["activities"], 1):
        if activity.strip():
            print(f"\n📌 Actividad {i}:")
            print(activity)
    
    print(f"\n👤 ID del estudiante: {result['student_id']}")
    return result

async def demo_model_training_tutor():
    """Demonstrate the ModelTrainingTutor functionality"""
    print("\n\n🧠 Inicializando Tutor de Entrenamiento de Modelos...")
    tutor = ModelTrainingTutor()
    
    result = await tutor.teach_topic(
        topic="machine learning básico",
        student_question="¿Qué es machine learning y cómo funciona?"
    )
    
    print("\n🎓 LECCIÓN:")
    print("=" * 50)
    print(result["answer"])
    
    return result

async def demo_data_collector():
    """Demonstrate the DataCollector functionality"""
    print("\n\n🔍 Demostrando Recolector de Datos...")
    try:
        collector = DataCollector()
        
        # Collect data about a programming topic
        data = await collector.collect_web_data("Python for beginners tutorial", 3)
        
        print(f"✅ Datos de Tavily: {len(data['tavily_data'])} resultados")
        print(f"✅ Datos de Exa: {len(data['exa_data'])} resultados")
        print(f"✅ Datos de Firecrawl: {len(data['firecrawl_data'])} resultados")
        
        # Extract unified content
        unified = collector.unified_content_extraction(data)
        print(f"✅ Contenido unificado: {len(unified)} documentos")
        
        return unified
    except Exception as e:
        print(f"❌ Error en recolección de datos: {e}")
        print("💡 Asegúrate de que las API keys estén configuradas en .env")
        return []

async def demo_knowledge_base(sample_content):
    """Demonstrate the KnowledgeBase functionality"""
    print("\n\n📚 Demostrando Base de Conocimientos...")
    try:
        kb = KnowledgeBase()
        
        if sample_content:
            # Add documents to knowledge base
            kb.add_documents(sample_content[:2])  # Add first 2 documents
            
            # Search the knowledge base
            results = kb.search("Python tutorial for beginners")
            print(f"✅ Búsqueda completada: {len(results)} resultados encontrados")
            
            if results:
                print("\n📖 Primer resultado:")
                print(f"Contenido: {results[0]['content'][:200]}...")
                print(f"Fuente: {results[0]['metadata']['source']}")
        else:
            print("⚠️ No hay contenido de muestra para agregar a la base de conocimientos")
            
    except Exception as e:
        print(f"❌ Error en base de conocimientos: {e}")

async def main():
    """Run the complete demo"""
    print("🚀 INICIANDO DEMOSTRACIÓN DE CLAUDE EDUCATION PLATFORM")
    print("=" * 60)
    
    try:
        # Demo 1: Chatbot Tutor
        chatbot_result = await demo_chatbot_tutor()
        
        # Demo 2: Model Training Tutor
        model_result = await demo_model_training_tutor()
        
        # Demo 3: Data Collector
        sample_content = await demo_data_collector()
        
        # Demo 4: Knowledge Base
        await demo_knowledge_base(sample_content)
        
        print("\n\n✅ DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
        print("🎯 Próximos pasos:")
        print("1. Configura tus API keys en el archivo .env")
        print("2. Ejecuta la aplicación Streamlit: streamlit run src/ui/app.py")
        print("3. ¡Comienza a aprender!")
        
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {e}")
        print("💡 Verifica que todas las dependencias estén instaladas:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    # Run the demo
    print("🎓 Bienvenido a Claude Education Platform")
    print("📋 Esta demostración mostrará las capacidades del sistema")
    print("\n⚠️  Nota: Necesitas configurar las API keys en .env para usar todas las funciones")
    
    asyncio.run(main())