"""
Caching Module
Handles caching of paper searches and results
"""

import json
import hashlib
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Cache:
    """Simple file-based cache"""
    
    def __init__(self, cache_dir: str = ".cache", ttl_seconds: int = 3600):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(seconds=ttl_seconds)
    
    def _get_cache_key(self, key: str) -> str:
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_cache_file(self, key: str) -> Path:
        return self.cache_dir / f"{self._get_cache_key(key)}.json"
    
    def get(self, key: str) -> Optional[Any]:
        try:
            cache_file = self._get_cache_file(key)
            if not cache_file.exists():
                return None
            
            with open(cache_file, 'r') as f:
                data = json.load(f)
            
            timestamp = datetime.fromisoformat(data['timestamp'])
            if datetime.now() - timestamp > self.ttl:
                cache_file.unlink()
                return None
            
            logger.debug(f"Cache hit for key: {key}")
            return data['value']
        except Exception as e:
            logger.error(f"Error reading cache: {e}")
            return None
    
    def set(self, key: str, value: Any) -> bool:
        try:
            cache_file = self._get_cache_file(key)
            data = {
                'timestamp': datetime.now().isoformat(),
                'value': value
            }
            with open(cache_file, 'w') as f:
                json.dump(data, f)
            logger.debug(f"Cache set for key: {key}")
            return True
        except Exception as e:
            logger.error(f"Error writing cache: {e}")
            return False
    
    def clear(self) -> bool:
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
            logger.info("Cache cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False

cache = Cache()

def get_cached(key: str) -> Optional[Any]:
    return cache.get(key)

def set_cache(key: str, value: Any) -> bool:
    return cache.set(key, value)

def clear_cache() -> bool:
    return cache.clear()
