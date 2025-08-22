import asyncio
from typing import List, Dict, Any
from firecrawl import FirecrawlApp
from exa_py import Exa
from tavily import TavilyClient
from config.settings import settings

class DataCollector:
    def __init__(self):
        self.firecrawl = FirecrawlApp(api_key=settings.firecrawl_api_key)
        self.exa = Exa(api_key=settings.exa_api_key)
        self.tavily = TavilyClient(api_key=settings.tavily_api_key)
    
    async def collect_web_data(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Collect data using all three tools"""
        results = {
            "firecrawl_data": [],
            "exa_data": [],
            "tavily_data": []
        }
        
        # Tavily Research (best for current/comprehensive info)
        try:
            tavily_response = self.tavily.search(
                query=query,
                search_depth="advanced",
                max_results=max_results
            )
            results["tavily_data"] = tavily_response.get("results", [])
        except Exception as e:
            print(f"Tavily error: {e}")
        
        # Exa Semantic Search (best for finding similar content)
        try:
            exa_response = self.exa.search(
                query=query,
                num_results=max_results,
                include_text=["summary"]
            )
            results["exa_data"] = [
                {
                    "url": result.url,
                    "title": result.title,
                    "text": result.summary,
                    "summary": result.summary
                }
                for result in exa_response.results
            ]
        except Exception as e:
            print(f"Exa error: {e}")
        
        # Firecrawl for specific URLs (best for deep scraping)
        urls_to_scrape = []
        for source in [results["tavily_data"], results["exa_data"]]:
            for item in source[:3]:  # Top 3 from each
                if isinstance(item, dict) and "url" in item:
                    urls_to_scrape.append(item["url"])
        
        for url in urls_to_scrape[:5]:  # Limit to 5 URLs
            try:
                scraped = self.firecrawl.scrape(url)
                if hasattr(scraped, 'markdown') and scraped.markdown:
                    results["firecrawl_data"].append({
                        "url": url,
                        "markdown": scraped.markdown,
                        "title": getattr(scraped, 'title', ''),
                        "content": scraped.markdown
                    })
            except Exception as e:
                print(f"Firecrawl error for {url}: {e}")
        
        return results

    def unified_content_extraction(self, collected_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract and unify content from all sources"""
        unified_content = []
        
        # Process Tavily data
        for item in collected_data["tavily_data"]:
            unified_content.append({
                "source": "tavily",
                "title": item.get("title", ""),
                "content": item.get("content", ""),
                "url": item.get("url", ""),
                "score": item.get("score", 0)
            })
        
        # Process Exa data
        for item in collected_data["exa_data"]:
            unified_content.append({
                "source": "exa",
                "title": item.get("title", ""),
                "content": item.get("text", ""),
                "url": item.get("url", ""),
                "highlights": item.get("highlights", [])
            })
        
        # Process Firecrawl data
        for item in collected_data["firecrawl_data"]:
            if item.get("success"):
                unified_content.append({
                    "source": "firecrawl",
                    "title": item.get("metadata", {}).get("title", ""),
                    "content": item.get("markdown", ""),
                    "url": item.get("metadata", {}).get("sourceURL", "")
                })
        
        return unified_content