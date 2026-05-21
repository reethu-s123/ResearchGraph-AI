"""
Advanced Configuration & Utilities
Real-time API utilities for ResearchGraph AI
"""

import asyncio
import aiohttp
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIClient:
    """Async API client for real-time queries"""
    
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Async GET request"""
        if not self.session:
            return None
        
        try:
            url = f"{self.base_url}/{endpoint}"
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                logger.error(f"API error: {response.status}")
                return None
        except Exception as e:
            logger.error(f"Request error: {e}")
            return None

class RealTimeManager:
    """Manages real-time paper updates"""
    
    def __init__(self):
        self.subscribers = []
        self.last_query = None
    
    def subscribe(self, callback):
        """Subscribe to updates"""
        self.subscribers.append(callback)
    
    async def publish_update(self, data: Dict):
        """Publish update to subscribers"""
        for callback in self.subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    async def stream_papers(self, query: str, callback):
        """Stream papers as they're retrieved"""
        async with APIClient("https://www.ebi.ac.uk/europepmc/webservices/rest") as client:
            page = 1
            while True:
                response = await client.get("search", {
                    "query": query,
                    "pageSize": 25,
                    "page": page,
                    "format": "json"
                })
                
                if not response:
                    break
                
                results = response.get("resultList", {}).get("result", [])
                if not results:
                    break
                
                for paper in results:
                    await self.publish_update({"type": "paper", "data": paper})
                
                page += 1
                await asyncio.sleep(0.5)  # Rate limiting

# Global instance
realtime_manager = RealTimeManager()
