from langchain_anthropic import ChatAnthropic
from src.rag.knowledge_base import KnowledgeBase
from src.rag.database import db_manager
from src.tools.data_collector import DataCollector
from config.settings import settings
from typing import Dict, List, Any
import asyncio
import uuid

class EducationalTutor:
    def __init__(self, subject: str = "AI and Programming"):
        self.subject = subject
        self.llm = ChatAnthropic(
            model=settings.claude_model,
            temperature=settings.temperature,
            api_key=settings.anthropic_api_key
        )
        self.kb = KnowledgeBase()
        self.data_collector = DataCollector()
        self.conversation_history = []
        
        self.system_prompt = f"""
You are an expert {subject} tutor for children and teenagers in Mexico City. 
Your goals:
- Teach AI, machine learning, and chatbot creation in an engaging way
- Use Socratic method - ask questions to guide discovery
- Explain complex concepts simply with analogies
- Encourage hands-on experimentation
- Be culturally aware and use Spanish terms when helpful
- Always be encouraging and patient

Teaching style:
- Never give direct answers - guide students to discover solutions
- Use local examples and cultural references when possible
- Break complex topics into digestible parts
- Celebrate small victories and progress
"""
    
    async def teach_topic(self, topic: str, student_question: str = None, student_id: str = None) -> Dict[str, Any]:
        """Main teaching method with RAG and web research"""
        
        if not student_id:
            student_id = str(uuid.uuid4())
        
        # Step 1: Search existing knowledge base
        kb_results = self.kb.search(topic)
        
        # Step 2: If insufficient context, gather new data
        if len(kb_results) < 3 or (kb_results and kb_results[0].get("distance", 1) > 0.7):
            print(f"Gathering fresh data about: {topic}")
            web_data = await self.data_collector.collect_web_data(
                query=f"{topic} tutorial programming kids beginners",
                max_results=8
            )
            
            unified_content = self.data_collector.unified_content_extraction(web_data)
            self.kb.add_documents(unified_content)
            
            # Search again with new data
            kb_results = self.kb.search(topic)
        
        # Step 3: Generate educational response
        if student_question:
            query = f"{topic}: {student_question}"
        else:
            query = f"How to teach {topic} to beginners"
            
        answer = self.kb.generate_answer(query, kb_results)
        
        # Step 4: Apply educational enhancements
        enhanced_answer = await self._enhance_for_education(answer, topic, student_question)
        
        # Step 5: Generate follow-up activities
        activities = await self._generate_activities(topic)
        
        # Step 6: Record interaction in database
        try:
            await db_manager.record_interaction(
                student_id=student_id,
                question=student_question or f"General topic: {topic}",
                answer=enhanced_answer,
                tutor_type=self.subject
            )
        except Exception as e:
            print(f"Database error: {e}")
        
        return {
            "answer": enhanced_answer,
            "activities": activities,
            "sources": [doc["metadata"] for doc in kb_results[:3]],
            "topic": topic,
            "student_id": student_id
        }
    
    async def _enhance_for_education(self, answer: str, topic: str, question: str = None) -> str:
        """Enhance answer with Socratic method and cultural context"""
        enhancement_prompt = f"""
Take this educational content and enhance it for Mexican students learning about AI:

Original content: {answer}
Topic: {topic}
Student question: {question or "General topic introduction"}

Enhance by:
1. Adding Socratic questions to guide thinking
2. Including simple analogies (preferably with Mexican cultural references)
3. Breaking into numbered steps for clarity
4. Adding encouragement and motivation
5. Suggesting hands-on experiments they can try
6. Using simple language appropriate for ages 10-16

System context: {self.system_prompt}

Enhanced educational response:"""
        
        response = self.llm.invoke(enhancement_prompt)
        return response.content
    
    async def _generate_activities(self, topic: str) -> List[str]:
        """Generate hands-on activities"""
        activity_prompt = f"""
Create 3 hands-on activities for students learning about {topic}.
Each activity should:
- Be doable with basic tools (computer, internet, maybe phone)
- Take 15-30 minutes
- Build practical skills
- Be fun and engaging
- Include clear steps

Activities for {topic}:"""
        
        response = self.llm.invoke(activity_prompt)
        activities = response.content.split('\n\n')
        return [activity.strip() for activity in activities if activity.strip()]

    async def record_progress(self, student_id: str, topic: str, completion_score: float, time_spent: int):
        """Record student progress"""
        try:
            return await db_manager.add_student_progress(student_id, topic, completion_score, time_spent)
        except Exception as e:
            print(f"Error recording progress: {e}")
            return None

    async def get_student_history(self, student_id: str):
        """Get student's learning history"""
        try:
            return await db_manager.get_student_progress(student_id)
        except Exception as e:
            print(f"Error getting student history: {e}")
            return []

# Specialized tutors
class ChatbotTutor(EducationalTutor):
    def __init__(self):
        super().__init__("Chatbot Development")
        self.system_prompt += """
        
Specialized focus on chatbots:
- Start with simple rule-based chatbots
- Progress to AI-powered conversational agents
- Emphasize understanding user intent
- Teach about conversation flow design
- Include practical examples like customer service bots
- Reference popular Mexican brands and services for examples
"""

class ModelTrainingTutor(EducationalTutor):
    def __init__(self):
        super().__init__("AI Model Training")
        self.system_prompt += """
        
Specialized focus on AI model training:
- Begin with concept of pattern recognition
- Use visual examples (recognizing tacos vs quesadillas)
- Explain data collection and preparation
- Introduce supervised vs unsupervised learning
- Demonstrate with simple tools like Teachable Machine
- Connect to real applications in Mexico (agriculture, tourism)
"""

class ProgrammingTutor(EducationalTutor):
    def __init__(self):
        super().__init__("Programming and AI")
        self.system_prompt += """
        
Specialized focus on programming for AI:
- Start with Python basics using AI-related examples
- Teach variables through AI concepts (storing user input)
- Explain functions through chatbot responses
- Use loops for training iterations
- Introduce libraries like requests for API calls
- Build toward creating simple AI applications
"""