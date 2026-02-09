"""Redis cache and rate limiting for AI features."""
import hashlib
from datetime import date

import redis

from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_cached(key: str) -> str | None:
    return redis_client.get(key)


def set_cached(key: str, value: str, ttl: int = 2592000) -> None:
    """Cache a value with TTL (default 30 days)."""
    redis_client.setex(key, ttl, value)


def make_cache_key(version: str, book: int, chapter: int, verse: int, question: str) -> str:
    """Create a deterministic cache key from verse reference + question."""
    q_hash = hashlib.sha256(question.lower().strip().encode()).hexdigest()[:16]
    return f"ai:verse:{version}:{book}:{chapter}:{verse}:{q_hash}"


def check_rate_limit(user_id: str, limit: int) -> tuple[bool, int]:
    """Check and increment daily rate limit for a user.

    Returns (allowed, remaining) where allowed is True if under the limit
    and remaining is how many questions are left today.
    """
    today = date.today().isoformat()
    key = f"rate_limit:ai:user:{user_id}:{today}"
    current = redis_client.get(key)
    count = int(current) if current else 0

    if count >= limit:
        return False, 0

    redis_client.incr(key)
    redis_client.expire(key, 86400)  # expire after 24h
    return True, limit - count - 1
