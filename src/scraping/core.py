"""
Core educational web scraper with intelligent content discovery
"""

import asyncio
import hashlib
import json
import logging
import re
import tiktoken
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse

from firecrawl import FirecrawlApp
from anthropic import Anthropic

from config.settings import settings
from src.scraping.cache import SmartCache
from src.scraping.rate_limiter import EducationalRateLimiter
from src.database.connection import get_db_manager

logger = logging.getLogger(__name__)

class EducationalScraper:
    """
    Advanced web scraper optimized for educational content discovery
    """
    
    def __init__(self, db_manager=None):
        self.firecrawl = FirecrawlApp(api_key=settings.firecrawl_api_key)
        self.anthropic = Anthropic(api_key=settings.anthropic_api_key)
        self.db = db_manager
        
        # Initialize components
        self.cache = SmartCache(db_manager)
        self.rate_limiter = EducationalRateLimiter()
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
        # Educational content patterns
        self.educational_patterns = {
            'tutorial_indicators': [
                'tutorial', 'guide', 'how-to', 'step-by-step', 'learn',
                'course', 'lesson', 'documentation', 'docs', 'example'
            ],
            'code_platforms': [
                'github.com', 'stackoverflow.com', 'codepen.io',
                'repl.it', 'codesandbox.io', 'jupyter.org'
            ],
            'educational_sites': [
                'coursera.org', 'edx.org', 'udemy.com', 'khanacademy.org',
                'freecodecamp.org', 'codecademy.com', 'pluralsight.com'
            ]
        }
        
        # Statistics tracking
        self.stats = {
            'total_scrapes': 0,
            'educational_content_found': 0,
            'cache_hits': 0,
            'total_cost': 0.0,
            'errors': 0
        }
    
    async def scrape_educational_content(
        self, 
        url: str,
        content_type: str = "tutorial",
        depth: int = 1,
        max_pages: int = 10
    ) -> Dict[str, Any]:
        """
        Scrape educational content with intelligent discovery
        
        Args:
            url: Starting URL for scraping
            content_type: Type of content to focus on (tutorial, documentation, course)
            depth: How many levels deep to crawl
            max_pages: Maximum pages to scrape
        
        Returns:
            Comprehensive educational content data
        """
        
        logger.info(f"🎓 Scraping educational content from {url}")
        
        result = {
            'source_url': url,
            'content_type': content_type,
            'pages_scraped': 0,
            'educational_content': [],
            'code_examples': [],
            'learning_objectives': [],
            'prerequisites': [],
            'difficulty_level': None,
            'estimated_time': None,
            'related_topics': [],
            'total_cost': 0.0,
            'error': None
        }
        
        try:
            # Apply rate limiting
            await self.rate_limiter.acquire('firecrawl')
            
            # Check cache first
            cached = await self.cache.get(url, f"educational_{content_type}")
            if cached:
                logger.info(f"📚 Using cached educational content for {url}")
                self.stats['cache_hits'] += 1
                return cached
            
            # Scrape main page with educational optimization
            main_content = await self._scrape_educational_page(url, content_type)
            
            if main_content['error']:
                result['error'] = main_content['error']
                return result
            
            result['pages_scraped'] += 1
            
            # Extract educational metadata
            educational_data = await self._extract_educational_metadata(
                main_content['content'], content_type
            )
            
            result.update(educational_data)
            result['educational_content'].append(main_content['content'])
            
            # Discover related educational pages if depth > 1
            if depth > 1 and result['pages_scraped'] < max_pages:
                related_urls = self._discover_related_educational_urls(
                    main_content['content'], url
                )
                
                for related_url in related_urls[:max_pages - result['pages_scraped']]:
                    try:
                        related_content = await self._scrape_educational_page(
                            related_url, content_type
                        )
                        
                        if not related_content['error']:
                            result['educational_content'].append(related_content['content'])
                            result['pages_scraped'] += 1
                            
                    except Exception as e:
                        logger.warning(f"Failed to scrape related URL {related_url}: {e}")
            
            # Cache successful results
            await self.cache.set(url, result, f"educational_{content_type}")
            
            # Update statistics
            self.stats['total_scrapes'] += 1
            self.stats['educational_content_found'] += len(result['educational_content'])
            
            logger.info(f"✅ Educational scraping complete: {result['pages_scraped']} pages")
            
        except Exception as e:
            logger.error(f"Educational scraping error for {url}: {e}")
            result['error'] = str(e)
            self.stats['errors'] += 1
        
        return result
    
    async def _scrape_educational_page(
        self, 
        url: str, 
        content_type: str
    ) -> Dict[str, Any]:
        """Scrape a single page optimized for educational content"""
        
        # Get optimized parameters for educational content
        params = self._get_educational_scrape_params(content_type)
        
        try:
            # Apply rate limiting
            await self.rate_limiter.acquire('firecrawl')
            
            # Scrape with Firecrawl
            scraped = self.firecrawl.scrape(url, params)
            
            if hasattr(scraped, 'markdown') and scraped.markdown:
                return {
                    'url': url,
                    'content': {
                        'markdown': scraped.markdown,
                        'title': getattr(scraped, 'title', ''),
                        'description': getattr(scraped, 'description', ''),
                        'metadata': getattr(scraped, 'metadata', {})
                    },
                    'error': None
                }
            else:
                return {
                    'url': url,
                    'content': None,
                    'error': 'No content extracted'
                }
                
        except Exception as e:
            logger.error(f"Scraping error for {url}: {e}")
            return {
                'url': url,
                'content': None,
                'error': str(e)
            }
    
    def _get_educational_scrape_params(self, content_type: str) -> Dict:
        """Get optimized scraping parameters for educational content"""
        
        base_params = {
            'formats': ['markdown'],
            'onlyMainContent': True,
            'removeBase64Images': True
        }
        
        if content_type == "tutorial":
            base_params.update({
                'includeTags': ['article', 'main', 'section', 'pre', 'code', 'h1', 'h2', 'h3', 'p', 'ol', 'ul'],
                'excludeTags': ['nav', 'footer', 'aside', 'advertisement'],
                'waitFor': 1000
            })
        elif content_type == "documentation":
            base_params.update({
                'includeTags': ['article', 'main', 'section', 'pre', 'code', 'table', 'dl'],
                'excludeTags': ['nav', 'footer', 'script', 'style'],
                'waitFor': 500
            })
        elif content_type == "course":
            base_params.update({
                'includeTags': ['article', 'main', 'section', 'video', 'h1', 'h2', 'h3'],
                'excludeTags': ['nav', 'footer', 'ads'],
                'waitFor': 2000
            })
        
        return base_params
    
    async def _extract_educational_metadata(
        self, 
        content: Dict, 
        content_type: str
    ) -> Dict[str, Any]:
        """Extract educational metadata using Claude AI"""
        
        markdown_content = content.get('markdown', '')
        
        # Compress content if too long
        if len(markdown_content) > 8000:
            markdown_content = markdown_content[:8000] + "\n\n[Content truncated for analysis]"
        
        # Create educational analysis prompt
        prompt = self._create_educational_analysis_prompt(markdown_content, content_type)
        
        try:
            # Apply rate limiting for Claude
            await self.rate_limiter.acquire('anthropic')
            
            # Analyze with Claude
            response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse Claude's structured response
            analysis = self._parse_educational_analysis(response.content[0].text)
            
            # Calculate cost
            input_tokens = len(self.tokenizer.encode(prompt))
            output_tokens = len(self.tokenizer.encode(response.content[0].text))
            cost = (input_tokens * 0.003 + output_tokens * 0.015) / 1000
            
            self.stats['total_cost'] += cost
            
            return analysis
            
        except Exception as e:
            logger.error(f"Educational analysis error: {e}")
            return {
                'code_examples': [],
                'learning_objectives': [],
                'prerequisites': [],
                'difficulty_level': 'unknown',
                'estimated_time': None,
                'related_topics': []
            }
    
    def _create_educational_analysis_prompt(
        self, 
        content: str, 
        content_type: str
    ) -> str:
        """Create prompt for educational content analysis"""
        
        return f"""
        Analyze this {content_type} content and extract educational metadata.
        Respond in JSON format with the following structure:
        
        {{
            "learning_objectives": ["objective1", "objective2"],
            "prerequisites": ["prerequisite1", "prerequisite2"],
            "difficulty_level": "beginner|intermediate|advanced",
            "estimated_time": "X minutes/hours",
            "code_examples": ["example1", "example2"],
            "related_topics": ["topic1", "topic2"],
            "key_concepts": ["concept1", "concept2"],
            "target_audience": "description of who this is for"
        }}
        
        Content to analyze:
        {content}
        
        Educational Analysis (JSON only):
        """
    
    def _parse_educational_analysis(self, analysis_text: str) -> Dict:
        """Parse Claude's educational analysis response"""
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                return parsed
        except Exception as e:
            logger.warning(f"Failed to parse educational analysis: {e}")
        
        # Fallback parsing
        return {
            'learning_objectives': self._extract_list_from_text(analysis_text, 'objectives?'),
            'prerequisites': self._extract_list_from_text(analysis_text, 'prerequisites?'),
            'difficulty_level': self._extract_difficulty(analysis_text),
            'estimated_time': self._extract_time_estimate(analysis_text),
            'code_examples': self._extract_code_examples(analysis_text),
            'related_topics': self._extract_list_from_text(analysis_text, 'topics?'),
            'key_concepts': [],
            'target_audience': 'general'
        }
    
    def _extract_list_from_text(self, text: str, pattern: str) -> List[str]:
        """Extract list items from text using regex"""
        
        items = []
        lines = text.split('\n')
        
        for line in lines:
            if re.search(pattern, line, re.IGNORECASE):
                # Extract bullet points or numbered items
                if any(marker in line for marker in ['-', '*', '•']):
                    item = re.sub(r'^[\s\-\*\•\d\.]+', '', line).strip()
                    if item:
                        items.append(item)
        
        return items[:5]  # Limit to 5 items
    
    def _extract_difficulty(self, text: str) -> str:
        """Extract difficulty level from text"""
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['beginner', 'basic', 'intro', 'getting started']):
            return 'beginner'
        elif any(word in text_lower for word in ['advanced', 'expert', 'complex']):
            return 'advanced'
        elif any(word in text_lower for word in ['intermediate', 'medium']):
            return 'intermediate'
        
        return 'unknown'
    
    def _extract_time_estimate(self, text: str) -> Optional[str]:
        """Extract time estimate from text"""
        
        time_pattern = r'(\d+)\s*(minutes?|hours?|mins?|hrs?)'
        match = re.search(time_pattern, text, re.IGNORECASE)
        
        if match:
            return f"{match.group(1)} {match.group(2)}"
        
        return None
    
    def _extract_code_examples(self, text: str) -> List[str]:
        """Extract code examples from markdown"""
        
        code_blocks = re.findall(r'```[\w]*\n(.*?)\n```', text, re.DOTALL)
        inline_code = re.findall(r'`([^`]+)`', text)
        
        examples = []
        examples.extend([block.strip() for block in code_blocks if len(block.strip()) > 10])
        examples.extend([code.strip() for code in inline_code if len(code.strip()) > 5])
        
        return examples[:10]  # Limit to 10 examples
    
    def _discover_related_educational_urls(
        self, 
        content: Dict, 
        base_url: str
    ) -> List[str]:
        """Discover related educational URLs from content"""
        
        markdown = content.get('markdown', '')
        base_domain = urlparse(base_url).netloc
        
        # Extract all URLs from markdown
        url_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(url_pattern, markdown)
        
        educational_urls = []
        
        for link_text, url in links:
            # Skip external links unless from known educational domains
            if url.startswith('http') and base_domain not in url:
                if not any(domain in url for domain in self.educational_patterns['educational_sites']):
                    continue
            
            # Convert relative URLs to absolute
            if not url.startswith('http'):
                url = urljoin(base_url, url)
            
            # Check if link text suggests educational content
            link_text_lower = link_text.lower()
            if any(indicator in link_text_lower for indicator in self.educational_patterns['tutorial_indicators']):
                educational_urls.append(url)
        
        return educational_urls[:5]  # Limit to 5 related URLs
    
    async def search_educational_content(
        self, 
        topic: str,
        content_types: List[str] = ["tutorial", "documentation"],
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for educational content on a specific topic
        
        Args:
            topic: Topic to search for
            content_types: Types of content to find
            max_results: Maximum number of results
        
        Returns:
            List of educational content results
        """
        
        logger.info(f"🔍 Searching educational content for: {topic}")
        
        results = []
        
        # Use existing data collector for web search
        from src.tools.data_collector import DataCollector
        
        collector = DataCollector()
        
        try:
            # Search with educational focus
            search_query = f"{topic} tutorial programming education learn"
            search_results = await collector.collect_web_data(search_query, max_results)
            
            # Process and filter results for educational content
            for source_type, data in search_results.items():
                if source_type == 'tavily_data':
                    for item in data[:max_results]:
                        # Score educational relevance
                        relevance_score = self._calculate_educational_relevance(item)
                        
                        if relevance_score > 0.5:  # Filter by relevance threshold
                            educational_result = {
                                'title': item.get('title', ''),
                                'url': item.get('url', ''),
                                'description': item.get('content', '')[:200],
                                'source': 'tavily',
                                'relevance_score': relevance_score,
                                'estimated_type': self._estimate_content_type(item)
                            }
                            results.append(educational_result)
            
            # Sort by relevance score
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            logger.info(f"✅ Found {len(results)} educational resources for {topic}")
            
        except Exception as e:
            logger.error(f"Educational search error: {e}")
        
        return results[:max_results]
    
    def _calculate_educational_relevance(self, item: Dict) -> float:
        """Calculate how relevant content is for education"""
        
        score = 0.0
        text = f"{item.get('title', '')} {item.get('content', '')}".lower()
        
        # Check for educational indicators
        for indicator in self.educational_patterns['tutorial_indicators']:
            if indicator in text:
                score += 0.1
        
        # Check for code-related content
        if any(term in text for term in ['code', 'programming', 'python', 'javascript', 'tutorial']):
            score += 0.2
        
        # Check for educational domains
        url = item.get('url', '')
        for domain in self.educational_patterns['educational_sites']:
            if domain in url:
                score += 0.3
                break
        
        # Check for learning-related keywords
        learning_keywords = ['learn', 'course', 'lesson', 'guide', 'example', 'practice']
        for keyword in learning_keywords:
            if keyword in text:
                score += 0.05
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _estimate_content_type(self, item: Dict) -> str:
        """Estimate the type of educational content"""
        
        text = f"{item.get('title', '')} {item.get('content', '')}".lower()
        
        if any(term in text for term in ['course', 'class', 'curriculum']):
            return 'course'
        elif any(term in text for term in ['docs', 'documentation', 'reference', 'api']):
            return 'documentation'
        elif any(term in text for term in ['tutorial', 'guide', 'how-to', 'walkthrough']):
            return 'tutorial'
        elif any(term in text for term in ['example', 'demo', 'sample']):
            return 'example'
        else:
            return 'general'
    
    def get_stats(self) -> Dict[str, Any]:
        """Get scraper statistics"""
        
        cache_stats = self.cache.get_stats()
        rate_stats = self.rate_limiter.get_stats()
        
        return {
            'scraper_stats': self.stats,
            'cache_stats': cache_stats,
            'rate_limiter_stats': rate_stats
        }