import redis.asyncio as redis
from app.core.config import get_settings

settings = get_settings()

redis_client = redis.from_url(
    settings.redis_url, #type: ignore
    decode_responses=True,
    socket_connect_timeout=5,   # 🔥 fail fast
    socket_timeout=5,           # 🔥 avoid hanging
)