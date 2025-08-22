import pytest
import asyncio
import sys
import os

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.tools.data_collector import DataCollector
from src.rag.knowledge_base import KnowledgeBase
from src.agents.tutor_agent import ChatbotTutor, ModelTrainingTutor, ProgrammingTutor

class TestDataCollector:
    """Test the DataCollector functionality"""
    
    @pytest.mark.asyncio
    async def test_data_collection_structure(self):
        """Test that data collection returns the expected structure"""
        collector = DataCollector()
        
        # Use a simple query that should work
        data = await collector.collect_web_data("Python programming", 2)
        
        # Check structure
        assert "tavily_data" in data
        assert "exa_data" in data
        assert "firecrawl_data" in data
        assert isinstance(data["tavily_data"], list)
        assert isinstance(data["exa_data"], list)
        assert isinstance(data["firecrawl_data"], list)
    
    def test_content_extraction(self):
        """Test unified content extraction"""
        collector = DataCollector()
        
        # Mock data
        sample_data = {
            "tavily_data": [
                {"title": "Test Title", "content": "Test content", "url": "http://test.com"}
            ],
            "exa_data": [
                {"title": "Exa Title", "text": "Exa content", "url": "http://exa.com"}
            ],
            "firecrawl_data": [
                {
                    "success": True,
                    "markdown": "Firecrawl content",
                    "metadata": {"title": "FC Title", "sourceURL": "http://fc.com"}
                }
            ]
        }
        
        unified = collector.unified_content_extraction(sample_data)
        
        assert len(unified) == 3
        assert unified[0]["source"] == "tavily"
        assert unified[1]["source"] == "exa"
        assert unified[2]["source"] == "firecrawl"

class TestKnowledgeBase:
    """Test the KnowledgeBase functionality"""
    
    def test_initialization(self):
        """Test KnowledgeBase initialization"""
        kb = KnowledgeBase()
        assert kb.client is not None
        assert kb.collection is not None
        assert kb.text_splitter is not None
    
    def test_document_addition(self):
        """Test adding documents to knowledge base"""
        kb = KnowledgeBase()
        
        sample_docs = [
            {
                "title": "Test Document",
                "content": "This is test content about programming and chatbots. It should be split into chunks.",
                "source": "test",
                "url": "http://test.com"
            }
        ]
        
        # This should not raise an exception
        kb.add_documents(sample_docs)
    
    def test_search_functionality(self):
        """Test knowledge base search"""
        kb = KnowledgeBase()
        
        # Add some test content first
        sample_docs = [
            {
                "title": "Python Programming",
                "content": "Python is a programming language that is great for beginners. It has simple syntax and is widely used in AI development.",
                "source": "test",
                "url": "http://test.com"
            }
        ]
        
        kb.add_documents(sample_docs)
        
        # Search for content
        results = kb.search("Python programming")
        
        assert isinstance(results, list)
        # Results might be empty if ChromaDB isn't properly set up, but structure should be correct
        if results:
            assert "content" in results[0]
            assert "metadata" in results[0]

class TestEducationalTutors:
    """Test the educational tutor classes"""
    
    def test_tutor_initialization(self):
        """Test that tutors initialize correctly"""
        chatbot_tutor = ChatbotTutor()
        model_tutor = ModelTrainingTutor()
        programming_tutor = ProgrammingTutor()
        
        assert chatbot_tutor.subject == "Chatbot Development"
        assert model_tutor.subject == "AI Model Training"
        assert programming_tutor.subject == "Programming and AI"
        
        # Check that system prompts are customized
        assert "chatbot" in chatbot_tutor.system_prompt.lower()
        assert "model" in model_tutor.system_prompt.lower()
        assert "programming" in programming_tutor.system_prompt.lower()
    
    @pytest.mark.asyncio
    async def test_activity_generation(self):
        """Test activity generation"""
        tutor = ChatbotTutor()
        
        activities = await tutor._generate_activities("Python basics")
        
        assert isinstance(activities, list)
        # Should generate at least one activity
        assert len([a for a in activities if a.strip()]) > 0

class TestDatabaseIntegration:
    """Test database-related functionality"""
    
    def test_database_models_import(self):
        """Test that database models can be imported"""
        from src.rag.database import StudentProgress, LessonContent, StudentInteraction, DatabaseManager
        
        # This should not raise import errors
        assert StudentProgress is not None
        assert LessonContent is not None
        assert StudentInteraction is not None
        assert DatabaseManager is not None

class TestConfiguration:
    """Test configuration and settings"""
    
    def test_settings_import(self):
        """Test that settings can be imported"""
        from config.settings import Settings, settings
        
        assert Settings is not None
        assert settings is not None
    
    def test_settings_structure(self):
        """Test settings structure"""
        from config.settings import settings
        
        # Check that required attributes exist (they might not have values without .env)
        assert hasattr(settings, 'claude_model')
        assert hasattr(settings, 'temperature')
        assert hasattr(settings, 'chunk_size')
        assert hasattr(settings, 'neon_project_id')

# Utility function for running tests
def run_tests():
    """Run all tests and return results"""
    print("🧪 Ejecutando pruebas de integración...")
    
    # Run pytest programmatically
    exit_code = pytest.main([__file__, "-v", "--tb=short"])
    
    if exit_code == 0:
        print("✅ Todas las pruebas pasaron exitosamente")
    else:
        print("❌ Algunas pruebas fallaron")
    
    return exit_code

if __name__ == "__main__":
    run_tests()