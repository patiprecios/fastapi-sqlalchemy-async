from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine


class EngineRepository:
    def __init__(self):
        self.engines = {
            'default': None
        }

    def create_engine(self, name: Optional[str] = None, *args, **kwargs) -> AsyncEngine:
        async_engine: AsyncEngine = create_async_engine(*args, **kwargs)

        self.engines[name] = async_engine

        return async_engine


default = EngineRepository()
