"""
DeepSeek Client for Claude Education Platform
Handles API connections, streaming, and model management
"""

import os
import json
import asyncio
import logging
from typing import Dict, List, Optional, Any, AsyncGenerator
from datetime import datetime
from openai import OpenAI, AsyncOpenAI
import yaml

logger = logging.getLogger(__name__)

class DeepSeekClient:
    """
    Client for interacting with DeepSeek models
    Supports both API and local inference
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize DeepSeek client
        
        Args:
            api_key: DeepSeek API key (can also be set via DEEPSEEK_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        
        if self.api_key:
            # API-based client for cloud models
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com"
            )
            self.async_client = AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com"
            )
            logger.info("✅ DeepSeek API client initialized")
        else:
            logger.warning("⚠️ No DeepSeek API key found. Only local models available.")
            self.client = None
            self.async_client = None
        
        # Load model configurations
        self.load_model_config()
        
        # Track usage for cost monitoring
        self.usage_tracker = {
            'total_input_tokens': 0,
            'total_output_tokens': 0,
            'total_cost': 0.0,
            'session_start': datetime.now()
        }
    
    def load_model_config(self):
        """Load model configurations from YAML file"""
        config_path = os.path.join(os.path.dirname(__file__), 'model_config.yaml')
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                self.models = config.get('models', {})
                self.profiles = config.get('profiles', {})
            logger.info(f"📚 Loaded {len(self.models)} model configurations")
        except Exception as e:
            logger.error(f"Error loading model config: {e}")
            self.models = {}
            self.profiles = {}
    
    def list_available_models(self) -> List[Dict[str, Any]]:
        """
        List all available models with their capabilities
        
        Returns:
            List of model information dictionaries
        """
        available = []
        
        for model_id, info in self.models.items():
            # Check if model is accessible
            is_available = False
            
            if info['provider'] == 'deepseek' and self.client:
                is_available = True
            elif info['provider'] in ['local_transformers', 'huggingface']:
                # Check if transformers is installed
                try:
                    import transformers
                    is_available = True
                except ImportError:
                    is_available = False
            
            available.append({
                'id': model_id,
                'name': info['display_name'],
                'description': info['description'],
                'provider': info['provider'],
                'available': is_available,
                'capabilities': info.get('capabilities', []),
                'best_for': info.get('best_for', ''),
                'cost': info.get('cost', {'input': 0, 'output': 0})
            })
        
        return available
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "deepseek-chat",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False
    ):
        """
        Send a chat request to DeepSeek
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model ID to use
            temperature: Creativity level (0-2)
            max_tokens: Maximum response length
            stream: Whether to stream the response
        
        Returns:
            Response text or generator for streaming
        """
        if not self.client:
            raise ValueError("DeepSeek API client not initialized. Please provide an API key.")
        
        try:
            if stream:
                return self._stream_chat(messages, model, temperature, max_tokens)
            else:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                # Track usage
                self._track_usage(response.usage, model)
                
                return response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"Chat error: {e}")
            raise
    
    def _stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int
    ):
        """Stream chat responses"""
        stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    async def async_chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "deepseek-chat",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False
    ):
        """
        Async version of chat for better performance
        """
        if not self.async_client:
            raise ValueError("DeepSeek API client not initialized. Please provide an API key.")
        
        if stream:
            return self._async_stream_chat(messages, model, temperature, max_tokens)
        else:
            response = await self.async_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            self._track_usage(response.usage, model)
            return response.choices[0].message.content
    
    async def _async_stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int
    ) -> AsyncGenerator[str, None]:
        """Async streaming chat"""
        stream = await self.async_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def _track_usage(self, usage, model: str):
        """Track token usage and costs"""
        if usage:
            input_tokens = usage.prompt_tokens
            output_tokens = usage.completion_tokens
            
            # Get cost info for model
            model_info = self.models.get(model, {})
            cost_info = model_info.get('cost', {'input': 0, 'output': 0})
            
            # Calculate cost (prices are per 1M tokens)
            input_cost = (input_tokens / 1_000_000) * cost_info['input']
            output_cost = (output_tokens / 1_000_000) * cost_info['output']
            total_cost = input_cost + output_cost
            
            # Update tracker
            self.usage_tracker['total_input_tokens'] += input_tokens
            self.usage_tracker['total_output_tokens'] += output_tokens
            self.usage_tracker['total_cost'] += total_cost
            
            logger.info(f"💰 Usage: {input_tokens} in, {output_tokens} out, ${total_cost:.6f}")
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        session_duration = (datetime.now() - self.usage_tracker['session_start']).total_seconds() / 60
        
        return {
            'total_input_tokens': self.usage_tracker['total_input_tokens'],
            'total_output_tokens': self.usage_tracker['total_output_tokens'],
            'total_tokens': self.usage_tracker['total_input_tokens'] + self.usage_tracker['total_output_tokens'],
            'total_cost': round(self.usage_tracker['total_cost'], 6),
            'session_duration_minutes': round(session_duration, 2)
        }
    
    def compare_models(
        self,
        prompt: str,
        models: List[str] = ["deepseek-chat", "deepseek-reasoner"],
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Compare responses from different models
        
        Args:
            prompt: The prompt to test
            models: List of model IDs to compare
            temperature: Temperature setting for all models
        
        Returns:
            Dictionary with model responses and metrics
        """
        results = {}
        
        for model_id in models:
            if model_id not in self.models:
                logger.warning(f"Model {model_id} not found in config")
                continue
            
            try:
                import time
                start_time = time.time()
                
                response = self.chat(
                    messages=[{"role": "user", "content": prompt}],
                    model=model_id,
                    temperature=temperature
                )
                
                response_time = time.time() - start_time
                
                results[model_id] = {
                    'response': response,
                    'response_time': round(response_time, 2),
                    'model_info': self.models[model_id],
                    'usage': self.get_usage_stats()
                }
                
            except Exception as e:
                results[model_id] = {
                    'error': str(e),
                    'model_info': self.models[model_id]
                }
        
        return results
    
    def get_recommended_model(self, task_type: str) -> str:
        """
        Get recommended model for a specific task
        
        Args:
            task_type: Type of task (e.g., 'beginner_coding', 'advanced_math')
        
        Returns:
            Recommended model ID
        """
        profile = self.profiles.get(task_type, {})
        recommended = profile.get('recommended_models', ['deepseek-chat'])
        
        # Return first available model from recommendations
        for model_id in recommended:
            if model_id in self.models:
                model_info = self.models[model_id]
                if model_info['provider'] == 'deepseek' and self.client:
                    return model_id
        
        # Fallback
        return profile.get('fallback', 'deepseek-chat')