"""
Educational rate limiter with intelligent backoff
"""

import asyncio
import logging
import random
import time
from collections import deque
from datetime import datetime, timedelta
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class EducationalRateLimiter:
    """
    Rate limiter optimized for educational content discovery
    """
    
    def __init__(self):
        # API-specific rate limits
        self.limits = {
            'firecrawl': {
                'requests_per_minute': 30,
                'requests_per_hour': 1000,
                'burst_limit': 5  # Allow 5 quick requests
            },
            'anthropic': {
                'requests_per_minute': 50,
                'requests_per_hour': 5000,
                'burst_limit': 10
            }
        }
        
        # Request tracking
        self.request_logs = {
            'firecrawl': {
                'minute': deque(),
                'hour': deque(),
                'burst': deque()
            },
            'anthropic': {
                'minute': deque(),
                'hour': deque(),
                'burst': deque()
            }
        }
        
        # Statistics
        self.stats = {
            'firecrawl': {
                'total_requests': 0,
                'total_wait_time': 0.0,
                'rate_limited': 0
            },
            'anthropic': {
                'total_requests': 0,
                'total_wait_time': 0.0,
                'rate_limited': 0
            }
        }
    
    async def acquire(self, api: str) -> float:
        """
        Acquire permission to make API request
        
        Args:
            api: API name ('firecrawl' or 'anthropic')
        
        Returns:
            Time waited in seconds
        """
        
        if api not in self.limits:
            raise ValueError(f"Unknown API: {api}")
        
        wait_time = await self._calculate_wait_time(api)
        
        if wait_time > 0:
            logger.info(f"Rate limiting {api}: waiting {wait_time:.1f}s")
            await asyncio.sleep(wait_time)
            self.stats[api]['rate_limited'] += 1
            self.stats[api]['total_wait_time'] += wait_time
        
        # Record this request
        now = datetime.now()
        self.request_logs[api]['minute'].append(now)
        self.request_logs[api]['hour'].append(now)
        self.request_logs[api]['burst'].append(now)
        
        self.stats[api]['total_requests'] += 1
        
        return wait_time
    
    async def _calculate_wait_time(self, api: str) -> float:
        """Calculate how long to wait before making request"""
        
        now = datetime.now()
        limits = self.limits[api]
        logs = self.request_logs[api]
        
        # Clean old requests
        self._clean_old_requests(api, now)
        
        wait_times = []
        
        # Check burst limit (last 10 seconds)
        if len(logs['burst']) >= limits['burst_limit']:
            burst_wait = 10 - (now - logs['burst'][0]).total_seconds()
            if burst_wait > 0:
                wait_times.append(burst_wait)
        
        # Check minute limit
        if len(logs['minute']) >= limits['requests_per_minute']:
            minute_wait = 60 - (now - logs['minute'][0]).total_seconds()
            if minute_wait > 0:
                wait_times.append(minute_wait)
        
        # Check hour limit
        if len(logs['hour']) >= limits['requests_per_hour']:
            hour_wait = 3600 - (now - logs['hour'][0]).total_seconds()
            if hour_wait > 0:
                wait_times.append(hour_wait)
        
        # Return the maximum wait time needed
        return max(wait_times) if wait_times else 0
    
    def _clean_old_requests(self, api: str, now: datetime) -> None:
        """Remove old request timestamps"""
        
        logs = self.request_logs[api]
        
        # Remove requests older than 10 seconds (burst)
        burst_cutoff = now - timedelta(seconds=10)
        while logs['burst'] and logs['burst'][0] < burst_cutoff:
            logs['burst'].popleft()
        
        # Remove requests older than 1 minute
        minute_cutoff = now - timedelta(minutes=1)
        while logs['minute'] and logs['minute'][0] < minute_cutoff:
            logs['minute'].popleft()
        
        # Remove requests older than 1 hour
        hour_cutoff = now - timedelta(hours=1)
        while logs['hour'] and logs['hour'][0] < hour_cutoff:
            logs['hour'].popleft()
    
    def get_current_usage(self, api: str) -> Dict:
        """Get current usage statistics for an API"""
        
        now = datetime.now()
        self._clean_old_requests(api, now)
        
        logs = self.request_logs[api]
        limits = self.limits[api]
        
        return {
            'burst_usage': f"{len(logs['burst'])}/{limits['burst_limit']}",
            'minute_usage': f"{len(logs['minute'])}/{limits['requests_per_minute']}",
            'hour_usage': f"{len(logs['hour'])}/{limits['requests_per_hour']}",
            'burst_available': limits['burst_limit'] - len(logs['burst']),
            'minute_available': limits['requests_per_minute'] - len(logs['minute']),
            'hour_available': limits['requests_per_hour'] - len(logs['hour'])
        }
    
    def get_stats(self) -> Dict:
        """Get comprehensive rate limiter statistics"""
        
        combined_stats = {}
        
        for api in self.stats:
            api_stats = self.stats[api].copy()
            
            # Calculate efficiency metrics
            total_requests = api_stats['total_requests']
            if total_requests > 0:
                api_stats['avg_wait_time'] = f"{api_stats['total_wait_time'] / total_requests:.2f}s"
                api_stats['rate_limit_percentage'] = f"{(api_stats['rate_limited'] / total_requests) * 100:.1f}%"
            else:
                api_stats['avg_wait_time'] = "0.00s"
                api_stats['rate_limit_percentage'] = "0.0%"
            
            # Add current usage
            api_stats['current_usage'] = self.get_current_usage(api)
            
            combined_stats[api] = api_stats
        
        return combined_stats
    
    async def wait_for_quota(self, api: str, required_requests: int) -> float:
        """
        Wait until we have quota for a specific number of requests
        
        Args:
            api: API name
            required_requests: Number of requests needed
        
        Returns:
            Time waited
        """
        
        if required_requests <= 0:
            return 0.0
        
        start_time = time.time()
        
        while True:
            usage = self.get_current_usage(api)
            
            # Check if we have enough quota
            if (usage['minute_available'] >= required_requests and 
                usage['hour_available'] >= required_requests):
                break
            
            # Wait a bit and check again
            await asyncio.sleep(1)
        
        total_wait = time.time() - start_time
        
        if total_wait > 1:
            logger.info(f"Waited {total_wait:.1f}s for {api} quota ({required_requests} requests)")
        
        return total_wait
    
    def estimate_completion_time(
        self, 
        api: str, 
        remaining_requests: int
    ) -> timedelta:
        """
        Estimate how long it will take to complete remaining requests
        
        Args:
            api: API name
            remaining_requests: Number of requests left to make
        
        Returns:
            Estimated completion time
        """
        
        if remaining_requests <= 0:
            return timedelta(0)
        
        limits = self.limits[api]
        usage = self.get_current_usage(api)
        
        # Calculate based on most restrictive limit
        requests_per_minute = limits['requests_per_minute']
        requests_per_hour = limits['requests_per_hour']
        
        # Estimate based on minute limit
        minutes_needed = remaining_requests / requests_per_minute
        
        # Estimate based on hour limit
        hours_needed = remaining_requests / requests_per_hour
        
        # Use the more conservative estimate
        if hours_needed * 60 > minutes_needed:
            # Hour limit is more restrictive
            return timedelta(hours=hours_needed)
        else:
            # Minute limit is more restrictive
            return timedelta(minutes=minutes_needed)


class RetryHandler:
    """
    Intelligent retry handler for educational scraping
    """
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        
        self.stats = {
            'total_attempts': 0,
            'successful_retries': 0,
            'failed_after_retries': 0,
            'immediate_successes': 0
        }
    
    async def execute_with_retry(
        self, 
        func, 
        *args, 
        retry_on: Optional[list] = None,
        **kwargs
    ):
        """
        Execute function with intelligent retry logic
        
        Args:
            func: Function to execute
            retry_on: List of error types/messages to retry on
            *args, **kwargs: Arguments for the function
        """
        
        if retry_on is None:
            retry_on = ['rate limit', '429', '503', '502', 'timeout', 'connection']
        
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            self.stats['total_attempts'] += 1
            
            try:
                result = await func(*args, **kwargs)
                
                if attempt == 0:
                    self.stats['immediate_successes'] += 1
                else:
                    self.stats['successful_retries'] += 1
                    logger.info(f"Success after {attempt} retries")
                
                return result
                
            except Exception as e:
                last_error = e
                error_msg = str(e).lower()
                
                # Check if we should retry
                should_retry = any(error_type.lower() in error_msg for error_type in retry_on)
                
                if not should_retry or attempt >= self.max_retries:
                    if attempt >= self.max_retries:
                        self.stats['failed_after_retries'] += 1
                    break
                
                # Calculate delay with exponential backoff and jitter
                delay = self._calculate_delay(attempt, error_msg)
                
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                logger.info(f"Retrying in {delay:.1f}s...")
                
                await asyncio.sleep(delay)
        
        # All retries exhausted
        logger.error(f"All {self.max_retries} retries failed for {func.__name__}")
        raise last_error
    
    def _calculate_delay(self, attempt: int, error_msg: str) -> float:
        """Calculate delay with exponential backoff and jitter"""
        
        # Base exponential backoff
        delay = min(self.base_delay * (2 ** attempt), 60)
        
        # Longer delay for rate limits
        if 'rate limit' in error_msg or '429' in error_msg:
            delay = min(delay * 2, 120)
        
        # Add jitter (±25%) to prevent thundering herd
        jitter = delay * 0.25 * (2 * random.random() - 1)
        
        return max(0.1, delay + jitter)
    
    def get_stats(self) -> Dict:
        """Get retry handler statistics"""
        
        total = max(1, self.stats['total_attempts'])
        
        return {
            **self.stats,
            'immediate_success_rate': f"{(self.stats['immediate_successes'] / total) * 100:.1f}%",
            'retry_success_rate': f"{(self.stats['successful_retries'] / max(1, self.stats['total_attempts'] - self.stats['immediate_successes'])) * 100:.1f}%"
        }