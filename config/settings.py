from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # API Keys
    anthropic_api_key: str
    firecrawl_api_key: str
    exa_api_key: str
    tavily_api_key: str
    deepseek_api_key: Optional[str] = None
    
    # Database
    database_url: str
    
    # Model Settings
    claude_model: str = "claude-3-5-sonnet-20241022"
    temperature: float = 0.7
    max_tokens: int = 4000
    
    # RAG Settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5
    
    # File paths
    knowledge_base_path: str = "data/knowledge_base"
    chroma_db_path: str = "data/chroma_db"
    
    # Neon Project Settings
    neon_project_id: str = "dark-heart-74010500"
    
    class Config:
        env_file = ".env"

settings = Settings()