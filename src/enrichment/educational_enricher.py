"""
Educational content enricher for curriculum enhancement
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from src.scraping.core import EducationalScraper
from src.database.connection import get_db_manager

logger = logging.getLogger(__name__)

class EducationalEnricher:
    """
    Enrich educational content for Mexican students learning programming and AI
    """
    
    def __init__(self, db_manager=None):
        self.scraper = EducationalScraper(db_manager)
        self.db = db_manager
        
        # Mexican cultural context for educational content
        self.cultural_context = {
            'language_preferences': ['spanish', 'english'],
            'local_examples': [
                'tacos vs quesadillas for ML classification',
                'México vs Estados Unidos for data comparison',
                'Peso mexicano for financial calculations',
                'CDMX, Guadalajara, Monterrey for location data'
            ],
            'educational_institutions': [
                'UNAM', 'Tecnológico de Monterrey', 'IPN', 'UAM'
            ],
            'tech_companies': [
                'Mercado Libre', 'Kavak', 'Clip', 'Konfío'
            ]
        }
        
        # Age-appropriate content mapping
        self.age_groups = {
            '10-16': {
                'complexity': 'beginner',
                'concepts': ['variables', 'loops', 'functions', 'basic_ai'],
                'projects': ['calculator', 'game', 'chatbot', 'image_classifier']
            },
            '14-18': {
                'complexity': 'intermediate',
                'concepts': ['data_structures', 'algorithms', 'ml_basics', 'web_dev'],
                'projects': ['web_app', 'ml_model', 'data_analysis', 'mobile_app']
            }
        }
    
    async def enrich_curriculum_topic(
        self, 
        topic: str,
        age_group: str = "10-16",
        language: str = "spanish"
    ) -> Dict[str, Any]:
        """
        Enrich a curriculum topic with relevant educational content
        
        Args:
            topic: Programming/AI topic to enrich
            age_group: Target age group (10-16 or 14-18)
            language: Preferred language (spanish or english)
        
        Returns:
            Enriched educational content
        """
        
        logger.info(f"🎓 Enriching curriculum topic: {topic} for age {age_group}")
        
        result = {
            'topic': topic,
            'age_group': age_group,
            'language': language,
            'tutorials': [],
            'examples': [],
            'exercises': [],
            'cultural_adaptations': [],
            'difficulty_progression': [],
            'estimated_learning_time': None,
            'prerequisites': [],
            'learning_objectives': [],
            'error': None
        }
        
        try:
            # Search for educational content
            search_results = await self.scraper.search_educational_content(
                topic=f"{topic} programming tutorial beginner",
                content_types=["tutorial", "documentation", "example"],
                max_results=15
            )
            
            # Process and categorize results
            categorized_content = self._categorize_educational_content(
                search_results, age_group
            )
            
            result.update(categorized_content)
            
            # Generate cultural adaptations
            cultural_adaptations = await self._generate_cultural_adaptations(
                topic, age_group, language
            )
            result['cultural_adaptations'] = cultural_adaptations
            
            # Create difficulty progression
            difficulty_progression = self._create_difficulty_progression(
                topic, age_group
            )
            result['difficulty_progression'] = difficulty_progression
            
            # Estimate learning time
            result['estimated_learning_time'] = self._estimate_learning_time(
                result, age_group
            )
            
            # Save enriched content to database
            await self._save_enriched_content(result)
            
            logger.info(f"✅ Successfully enriched {topic} with {len(result['tutorials'])} tutorials")
            
        except Exception as e:
            logger.error(f"Error enriching curriculum topic {topic}: {e}")
            result['error'] = str(e)
        
        return result
    
    def _categorize_educational_content(
        self, 
        search_results: List[Dict], 
        age_group: str
    ) -> Dict[str, List]:
        """Categorize search results into educational content types"""
        
        categorized = {
            'tutorials': [],
            'examples': [],
            'exercises': [],
            'prerequisites': [],
            'learning_objectives': []
        }
        
        age_config = self.age_groups.get(age_group, self.age_groups['10-16'])
        target_complexity = age_config['complexity']
        
        for result in search_results:
            content_item = {
                'title': result['title'],
                'url': result['url'],
                'description': result['description'],
                'relevance_score': result['relevance_score'],
                'estimated_type': result['estimated_type'],
                'difficulty': self._estimate_difficulty(result),
                'suitable_for_age': self._is_suitable_for_age(result, age_group)
            }
            
            # Only include content suitable for age group
            if not content_item['suitable_for_age']:
                continue
            
            # Categorize based on estimated type and content
            if result['estimated_type'] == 'tutorial':
                categorized['tutorials'].append(content_item)
            elif result['estimated_type'] == 'example':
                categorized['examples'].append(content_item)
            elif 'exercise' in result['title'].lower() or 'practice' in result['title'].lower():
                categorized['exercises'].append(content_item)
        
        # Sort by relevance score
        for category in categorized:
            if isinstance(categorized[category], list):
                categorized[category].sort(
                    key=lambda x: x.get('relevance_score', 0), 
                    reverse=True
                )
        
        return categorized
    
    def _estimate_difficulty(self, content: Dict) -> str:
        """Estimate content difficulty level"""
        
        text = f"{content['title']} {content['description']}".lower()
        
        beginner_indicators = [
            'beginner', 'basic', 'intro', 'getting started', 
            'fundamentals', 'first', 'simple'
        ]
        
        advanced_indicators = [
            'advanced', 'expert', 'complex', 'deep dive',
            'master', 'professional', 'optimization'
        ]
        
        intermediate_indicators = [
            'intermediate', 'next level', 'beyond basics'
        ]
        
        if any(indicator in text for indicator in beginner_indicators):
            return 'beginner'
        elif any(indicator in text for indicator in advanced_indicators):
            return 'advanced'
        elif any(indicator in text for indicator in intermediate_indicators):
            return 'intermediate'
        
        return 'unknown'
    
    def _is_suitable_for_age(self, content: Dict, age_group: str) -> bool:
        """Check if content is suitable for the target age group"""
        
        difficulty = self._estimate_difficulty(content)
        age_config = self.age_groups.get(age_group, self.age_groups['10-16'])
        
        # Map age groups to suitable difficulties
        if age_group == '10-16':
            suitable_difficulties = ['beginner', 'unknown']
        elif age_group == '14-18':
            suitable_difficulties = ['beginner', 'intermediate', 'unknown']
        else:
            suitable_difficulties = ['beginner', 'intermediate', 'advanced', 'unknown']
        
        return difficulty in suitable_difficulties
    
    async def _generate_cultural_adaptations(
        self, 
        topic: str, 
        age_group: str, 
        language: str
    ) -> List[Dict]:
        """Generate Mexican cultural adaptations for the topic"""
        
        adaptations = []
        
        # Create culturally relevant examples
        if topic.lower() in ['variables', 'data types']:
            adaptations.append({
                'type': 'example',
                'title': 'Variables con nombres mexicanos',
                'content': 'nombre_estudiante = "María", edad = 15, ciudad = "Guadalajara"',
                'explanation': 'Usar nombres y lugares familiares para explicar variables'
            })
        
        elif topic.lower() in ['functions', 'funciones']:
            adaptations.append({
                'type': 'example',
                'title': 'Función para calcular el precio de tacos',
                'content': 'def calcular_precio_tacos(cantidad, precio_por_taco=15): return cantidad * precio_por_taco',
                'explanation': 'Ejemplo práctico usando precios en pesos mexicanos'
            })
        
        elif topic.lower() in ['lists', 'arrays', 'listas']:
            adaptations.append({
                'type': 'example',
                'title': 'Lista de estados mexicanos',
                'content': 'estados = ["CDMX", "Jalisco", "Nuevo León", "Yucatán"]',
                'explanation': 'Usar datos geográficos conocidos para enseñar listas'
            })
        
        elif topic.lower() in ['machine learning', 'ml', 'clasificación']:
            adaptations.append({
                'type': 'project',
                'title': 'Clasificador de comida mexicana',
                'content': 'Crear un modelo que distinga entre tacos, quesadillas y tortas',
                'explanation': 'Proyecto de ML con comida familiar para los estudiantes'
            })
        
        # Add language-specific adaptations
        if language == 'spanish':
            for adaptation in adaptations:
                adaptation['language_notes'] = 'Explicar términos técnicos en español con equivalentes en inglés'
        
        return adaptations
    
    def _create_difficulty_progression(
        self, 
        topic: str, 
        age_group: str
    ) -> List[Dict]:
        """Create a difficulty progression for the topic"""
        
        age_config = self.age_groups.get(age_group, self.age_groups['10-16'])
        
        progression = [
            {
                'level': 'Introducción',
                'description': f'Conceptos básicos de {topic}',
                'activities': ['Lectura', 'Ejemplos simples', 'Explicación visual'],
                'time_estimate': '30 minutos'
            },
            {
                'level': 'Práctica guiada',
                'description': f'Ejercicios paso a paso de {topic}',
                'activities': ['Seguir tutorial', 'Modificar ejemplos', 'Preguntas'],
                'time_estimate': '45 minutos'
            },
            {
                'level': 'Práctica independiente',
                'description': f'Crear proyectos propios con {topic}',
                'activities': ['Proyecto personal', 'Experimentación', 'Depuración'],
                'time_estimate': '60 minutos'
            }
        ]
        
        # Add advanced level for older students
        if age_group == '14-18':
            progression.append({
                'level': 'Aplicación avanzada',
                'description': f'Integrar {topic} en proyectos complejos',
                'activities': ['Proyecto colaborativo', 'Optimización', 'Documentación'],
                'time_estimate': '90 minutos'
            })
        
        return progression
    
    def _estimate_learning_time(self, content: Dict, age_group: str) -> str:
        """Estimate total learning time for the enriched content"""
        
        base_time = 120  # 2 hours base
        
        # Adjust based on content amount
        tutorial_count = len(content.get('tutorials', []))
        example_count = len(content.get('examples', []))
        exercise_count = len(content.get('exercises', []))
        
        additional_time = (tutorial_count * 20) + (example_count * 10) + (exercise_count * 15)
        
        # Adjust based on age group
        if age_group == '10-16':
            additional_time *= 1.3  # Younger students need more time
        
        total_minutes = base_time + additional_time
        
        if total_minutes < 120:
            return f"{total_minutes} minutos"
        else:
            hours = total_minutes // 60
            minutes = total_minutes % 60
            return f"{hours} horas {minutes} minutos"
    
    async def _save_enriched_content(self, content: Dict) -> None:
        """Save enriched content to database"""
        
        try:
            if not self.db:
                self.db = await get_db_manager()
                
            await self.db.save_research_source(
                topic=content['topic'],
                age_group=content['age_group'],
                language=content['language'],
                content_data=content,
                tutorial_count=len(content.get('tutorials', [])),
                example_count=len(content.get('examples', [])),
                estimated_time=content['estimated_learning_time']
            )
            
            logger.info(f"💾 Saved enriched content for {content['topic']} to database")
            
        except Exception as e:
            logger.error(f"Error saving enriched content: {e}")
    
    async def enrich_multiple_topics(
        self, 
        topics: List[str],
        age_group: str = "10-16",
        language: str = "spanish"
    ) -> List[Dict]:
        """Enrich multiple curriculum topics concurrently"""
        
        logger.info(f"📚 Enriching {len(topics)} topics for age group {age_group}")
        
        # Process topics concurrently with a reasonable limit
        semaphore = asyncio.Semaphore(3)
        
        async def enrich_with_limit(topic):
            async with semaphore:
                return await self.enrich_curriculum_topic(topic, age_group, language)
        
        tasks = [enrich_with_limit(topic) for topic in topics]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        enriched_topics = []
        for topic, result in zip(topics, results):
            if isinstance(result, Exception):
                enriched_topics.append({
                    'topic': topic,
                    'error': str(result)
                })
            else:
                enriched_topics.append(result)
        
        # Generate summary
        successful = len([r for r in enriched_topics if not r.get('error')])
        total_tutorials = sum(len(r.get('tutorials', [])) for r in enriched_topics)
        
        logger.info(f"✅ Enrichment complete: {successful}/{len(topics)} topics")
        logger.info(f"📖 Total tutorials found: {total_tutorials}")
        
        return enriched_topics
    
    async def get_enrichment_suggestions(
        self, 
        current_lesson: str,
        student_progress: Dict
    ) -> List[Dict]:
        """Get enrichment suggestions based on current lesson and student progress"""
        
        suggestions = []
        
        try:
            # Analyze student's current level
            difficulty_level = self._analyze_student_level(student_progress)
            
            # Search for related content
            related_content = await self.scraper.search_educational_content(
                topic=f"{current_lesson} next steps advanced",
                max_results=5
            )
            
            for content in related_content:
                if content['relevance_score'] > 0.7:
                    suggestions.append({
                        'title': content['title'],
                        'url': content['url'],
                        'type': 'extension',
                        'difficulty': self._estimate_difficulty(content),
                        'why_suggested': f"Builds on {current_lesson} concepts",
                        'estimated_time': '30-45 minutos'
                    })
            
            # Add cultural project suggestions
            cultural_projects = self._get_cultural_project_suggestions(current_lesson)
            suggestions.extend(cultural_projects)
            
        except Exception as e:
            logger.error(f"Error getting enrichment suggestions: {e}")
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def _analyze_student_level(self, progress: Dict) -> str:
        """Analyze student's learning level from progress data"""
        
        completed_lessons = progress.get('completed_lessons', 0)
        average_score = progress.get('average_score', 0)
        
        if completed_lessons < 5 or average_score < 70:
            return 'beginner'
        elif completed_lessons < 15 or average_score < 85:
            return 'intermediate'
        else:
            return 'advanced'
    
    def _get_cultural_project_suggestions(self, lesson: str) -> List[Dict]:
        """Get culturally relevant project suggestions"""
        
        cultural_projects = {
            'variables': {
                'title': 'Calculadora de propinas mexicanas',
                'description': 'Crear una calculadora que calcule propinas en restaurantes mexicanos',
                'cultural_element': 'Usar porcentajes de propina comunes en México'
            },
            'functions': {
                'title': 'Conversor de peso a dólar',
                'description': 'Función que convierte pesos mexicanos a dólares',
                'cultural_element': 'Usar tipos de cambio reales'
            },
            'lists': {
                'title': 'Organizador de festivales mexicanos',
                'description': 'Lista y organiza festivales por estado',
                'cultural_element': 'Usar festivales reales de cada estado'
            },
            'machine learning': {
                'title': 'Reconocedor de música regional',
                'description': 'Clasificar diferentes géneros de música mexicana',
                'cultural_element': 'Mariachi, norteño, banda, ranchera'
            }
        }
        
        suggestions = []
        lesson_lower = lesson.lower()
        
        for key, project in cultural_projects.items():
            if key in lesson_lower:
                suggestions.append({
                    'title': project['title'],
                    'type': 'cultural_project',
                    'description': project['description'],
                    'cultural_element': project['cultural_element'],
                    'estimated_time': '2-3 horas',
                    'why_suggested': f"Aplica conceptos de {lesson} con contexto mexicano"
                })
        
        return suggestions