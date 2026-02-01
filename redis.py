import redis.asyncio as redis
from app.core.config import settings
from typing import Optional

class RedisClient:
    client: Optional[redis.Redis] = None
    
    @classmethod
    async def connect(cls):
        """Connect to Redis."""
        cls.client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=50
        )
        # Test connection
        await cls.client.ping()
        print("✓ Connected to Redis")
    
    @classmethod
    async def close(cls):
        """Close Redis connection."""
        if cls.client:
            await cls.client.close()
            print("✓ Closed Redis connection")
    
    @classmethod
    def get_client(cls) -> redis.Redis:
        """Get Redis client instance."""
        if not cls.client:
            raise RuntimeError("Redis not connected")
        return cls.client


def get_redis() -> redis.Redis:
    """Get Redis client."""
    return RedisClient.get_client()


async def init_redis():
    """Initialize Redis connection."""
    await RedisClient.connect()
