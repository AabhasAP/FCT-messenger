from fastapi import Request, HTTPException, status
from typing import Optional
import time
from app.core.config import settings


class RateLimiter:
    """Redis-based rate limiter for API endpoints."""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.per_minute = settings.RATE_LIMIT_PER_MINUTE
        self.per_hour = settings.RATE_LIMIT_PER_HOUR
    
    async def check_rate_limit(
        self, 
        key: str, 
        limit: int, 
        window: int
    ) -> bool:
        """
        Check if rate limit is exceeded.
        
        Args:
            key: Unique identifier (e.g., user_id, ip_address)
            limit: Maximum number of requests
            window: Time window in seconds
        
        Returns:
            True if within limit, raises HTTPException if exceeded
        """
        current_time = int(time.time())
        window_key = f"rate_limit:{key}:{current_time // window}"
        
        try:
            # Increment counter
            count = await self.redis.incr(window_key)
            
            # Set expiry on first request
            if count == 1:
                await self.redis.expire(window_key, window)
            
            if count > limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Maximum {limit} requests per {window} seconds.",
                    headers={"Retry-After": str(window)}
                )
            
            return True
        except HTTPException:
            raise
        except Exception as e:
            # If Redis fails, allow the request (fail open)
            print(f"Rate limiter error: {e}")
            return True
    
    async def check_user_rate_limit(self, user_id: str) -> bool:
        """Check rate limit for a specific user."""
        # Check per-minute limit
        await self.check_rate_limit(f"user:{user_id}", self.per_minute, 60)
        # Check per-hour limit
        await self.check_rate_limit(f"user:{user_id}:hour", self.per_hour, 3600)
        return True
    
    async def check_ip_rate_limit(self, ip_address: str) -> bool:
        """Check rate limit for an IP address."""
        await self.check_rate_limit(f"ip:{ip_address}", self.per_minute * 2, 60)
        return True


async def get_client_ip(request: Request) -> str:
    """Extract client IP from request."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"
