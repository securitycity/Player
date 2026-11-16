from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from src.config import settings
from redis import asyncio as aioredis


db_url = settings.DB_URL
engine = create_async_engine(db_url, connect_args={"server_settings" : {"jits": "off"}})
pg_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)

EDIS_URL = f"redis://{settings.REDIS_HOSTNAME}:{settings.REDIS_PORT}"
redis = aioredis.Redis.from_url(url=REDIS_URL)
