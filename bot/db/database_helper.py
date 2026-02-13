import os

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from .models import Base

PATH = "data/"

engine: AsyncEngine = create_async_engine(url=f"sqlite+aiosqlite:///{PATH}db.sqlite3")


def create_folder(path: str) -> None:
    os.makedirs(path, exist_ok=True)


async def init_models() -> None:
    create_folder(PATH)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
