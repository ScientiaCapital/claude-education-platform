"""
Smart caching system for educational web scraping
"""

import hashlib
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)

class SmartCache:
    """
    Multi-tier caching system optimized for educational content
    """
    
    def __init__(self, db_manager=None, cache_dir: str = "cache/educational"):
        self.db = db_manager
        self.cache_dir = Path(cache_dir)
        self.memory_cache = {}  # In-memory cache for current session
        
        # Create cache directories
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        for subdir in ["tutorials", "documentation", "courses", "searches"]:
            (self.cache_dir / subdir).mkdir(exist_ok=True)
        
        # Cache statistics
        self.stats = {
            "hits": 0,
            "misses": 0,
            "saves": 0,
            "memory_size": 0,
            "estimated_savings": 0.0
        }
    
    def _generate_cache_key(self, url: str, params: Dict = None) -> str:
        """Generate unique cache key for URL and parameters"""
        
        cache_input = f"{url}:{json.dumps(params or {}, sort_keys=True)}"
        return hashlib.md5(cache_input.encode()).hexdigest()
    
    async def get(
        self, 
        url: str, 
        cache_type: str = "tutorials",
        max_age_hours: int = 24
    ) -> Optional[Dict]:
        """
        Retrieve cached educational content
        
        Priority: memory → database → file
        """
        
        cache_key = self._generate_cache_key(url)
        
        # 1. Check memory cache
        if cache_key in self.memory_cache:
            cached = self.memory_cache[cache_key]
            if self._is_valid(cached, max_age_hours):
                self.stats["hits"] += 1
                logger.debug(f"Cache hit (memory): {url}")
                return cached["data"]
            else:
                # Remove expired entry
                del self.memory_cache[cache_key]
        
        # 2. Check database cache
        if self.db:
            try:
                db_cache = await self._get_from_database(cache_key)
                if db_cache and self._is_valid(db_cache, max_age_hours):
                    # Populate memory cache
                    self.memory_cache[cache_key] = db_cache
                    self.stats["hits"] += 1
                    logger.debug(f"Cache hit (database): {url}")
                    return db_cache["data"]
            except Exception as e:
                logger.warning(f"Database cache error: {e}")
        
        # 3. Check file cache
        file_path = self.cache_dir / cache_type / f"{cache_key}.json"
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    cached = json.load(f)
                
                if self._is_valid(cached, max_age_hours):
                    # Populate higher-tier caches
                    self.memory_cache[cache_key] = cached
                    
                    if self.db:
                        await self._save_to_database(cache_key, cached, cache_type, url)
                    
                    self.stats["hits"] += 1
                    logger.debug(f"Cache hit (file): {url}")
                    return cached["data"]
                else:
                    # Remove expired file
                    file_path.unlink()
                    
            except Exception as e:
                logger.warning(f"File cache read error: {e}")
                # Remove corrupted file
                try:
                    file_path.unlink()
                except:
                    pass
        
        # Cache miss
        self.stats["misses"] += 1
        logger.debug(f"Cache miss: {url}")
        return None
    
    async def set(
        self, 
        url: str, 
        data: Dict, 
        cache_type: str = "tutorials"
    ) -> None:
        """
        Save educational content to all cache tiers
        """
        
        cache_key = self._generate_cache_key(url)
        
        cached_entry = {
            "url": url,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "cache_type": cache_type,
            "size": len(json.dumps(data))
        }
        
        # 1. Save to memory cache
        self.memory_cache[cache_key] = cached_entry
        self.stats["memory_size"] = len(self.memory_cache)
        
        # 2. Save to database
        if self.db:
            try:
                await self._save_to_database(cache_key, cached_entry, cache_type, url)
            except Exception as e:
                logger.warning(f"Database cache save error: {e}")
        
        # 3. Save to file
        file_path = self.cache_dir / cache_type / f"{cache_key}.json"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(cached_entry, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"File cache save error: {e}")
        
        self.stats["saves"] += 1
        logger.debug(f"Cached educational content: {url}")
    
    def _is_valid(self, cached: Dict, max_age_hours: int) -> bool:
        """Check if cached entry is still valid"""
        
        if not cached or "timestamp" not in cached:
            return False
        
        try:
            cached_time = datetime.fromisoformat(cached["timestamp"])
            age = datetime.now() - cached_time
            return age < timedelta(hours=max_age_hours)
        except Exception:
            return False
    
    async def _get_from_database(self, cache_key: str) -> Optional[Dict]:
        """Get cache entry from database"""
        
        if not self.db:
            return None
        
        try:
            # Using the database manager's get_cache method
            result = await self.db.get_cache(cache_key)
            
            if result:
                return {
                    "data": result,
                    "timestamp": datetime.now().isoformat()  # Approximate
                }
        except Exception as e:
            logger.warning(f"Database cache get error: {e}")
        
        return None
    
    async def _save_to_database(
        self, 
        cache_key: str, 
        cached_entry: Dict, 
        cache_type: str,
        url: str
    ) -> None:
        """Save cache entry to database"""
        
        if not self.db:
            return
        
        try:
            await self.db.set_cache(
                cache_key=cache_key,
                cache_type=f"educational_{cache_type}",
                data=cached_entry["data"],
                expires_hours=24,  # Default 24 hours
                url=url
            )
        except Exception as e:
            logger.warning(f"Database cache save error: {e}")
    
    async def invalidate(self, url: str, cache_type: str = "tutorials") -> None:
        """
        Invalidate cache for a specific URL
        """
        
        cache_key = self._generate_cache_key(url)
        
        # Remove from memory
        if cache_key in self.memory_cache:
            del self.memory_cache[cache_key]
        
        # Remove from file cache
        file_path = self.cache_dir / cache_type / f"{cache_key}.json"
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                logger.warning(f"File cache invalidation error: {e}")
        
        # Remove from database
        if self.db:
            try:
                await self.db.execute(
                    "DELETE FROM cache_entries WHERE cache_key = $1",
                    cache_key
                )
            except Exception as e:
                logger.warning(f"Database cache invalidation error: {e}")
        
        logger.info(f"Invalidated cache for: {url}")
    
    async def cleanup_expired(self, max_age_days: int = 7) -> int:
        """
        Clean up expired cache entries
        
        Returns:
            Number of entries cleaned up
        """
        
        cleaned_count = 0
        cutoff_time = datetime.now() - timedelta(days=max_age_days)
        
        # Clean memory cache
        expired_keys = []
        for key, entry in self.memory_cache.items():
            if not self._is_valid(entry, max_age_days * 24):
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.memory_cache[key]
            cleaned_count += 1
        
        # Clean file cache
        for cache_type_dir in self.cache_dir.iterdir():
            if cache_type_dir.is_dir():
                for cache_file in cache_type_dir.glob("*.json"):
                    try:
                        with open(cache_file, 'r', encoding='utf-8') as f:
                            cached = json.load(f)
                        
                        if not self._is_valid(cached, max_age_days * 24):
                            cache_file.unlink()
                            cleaned_count += 1
                            
                    except Exception:
                        # Remove corrupted files
                        cache_file.unlink()
                        cleaned_count += 1
        
        # Clean database cache
        if self.db:
            try:
                db_cleaned = await self.db.cleanup_expired_cache()
                cleaned_count += db_cleaned
            except Exception as e:
                logger.warning(f"Database cache cleanup error: {e}")
        
        logger.info(f"Cleaned up {cleaned_count} expired cache entries")
        return cleaned_count
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / max(1, total_requests)) * 100
        
        # Estimate cost savings (assuming $0.0001 per scrape)
        estimated_savings = self.stats["hits"] * 0.0001
        
        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "saves": self.stats["saves"],
            "hit_rate": f"{hit_rate:.1f}%",
            "memory_entries": len(self.memory_cache),
            "memory_size_mb": sum(
                entry.get("size", 0) for entry in self.memory_cache.values()
            ) / 1024 / 1024,
            "estimated_savings": f"${estimated_savings:.4f}",
            "total_requests": total_requests
        }
    
    async def get_cache_summary(self) -> Dict[str, Any]:
        """Get comprehensive cache summary"""
        
        summary = {
            "memory_cache": {
                "entries": len(self.memory_cache),
                "types": {}
            },
            "file_cache": {
                "total_files": 0,
                "types": {}
            },
            "database_cache": {
                "status": "unavailable"
            }
        }
        
        # Analyze memory cache
        for entry in self.memory_cache.values():
            cache_type = entry.get("cache_type", "unknown")
            summary["memory_cache"]["types"][cache_type] = \
                summary["memory_cache"]["types"].get(cache_type, 0) + 1
        
        # Analyze file cache
        for cache_type_dir in self.cache_dir.iterdir():
            if cache_type_dir.is_dir():
                file_count = len(list(cache_type_dir.glob("*.json")))
                summary["file_cache"]["types"][cache_type_dir.name] = file_count
                summary["file_cache"]["total_files"] += file_count
        
        # Check database cache status
        if self.db:
            try:
                db_count = await self.db.fetchval(
                    "SELECT COUNT(*) FROM cache_entries WHERE cache_type LIKE 'educational_%'"
                )
                summary["database_cache"] = {
                    "status": "available",
                    "entries": db_count or 0
                }
            except Exception:
                summary["database_cache"]["status"] = "error"
        
        return summary