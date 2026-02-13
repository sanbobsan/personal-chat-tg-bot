from typing import Tuple

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from .database_helper import engine
from .models import User


async def create_user(user_id: int, name: str) -> None:
    async with AsyncSession(engine) as session:
        new_user = User(user_id=user_id, name=name)
        session.add(new_user)
        await session.commit()


async def _get_user(session: AsyncSession, user_id: int) -> User | None:
    statement: Select[Tuple[User]] = select(User).where(User.user_id == user_id)
    user: User | None = await session.scalar(statement)
    return user


async def read_user(user_id: int) -> User | None:
    async with AsyncSession(engine) as session:
        user: User | None = await _get_user(session, user_id)
    return user


async def update_user(user_id: int, **kwds) -> User | None:
    async with AsyncSession(engine) as session:
        user: User | None = await _get_user(session, user_id)
        for key, value in kwds.items():
            setattr(user, key, value)
        await session.commit()
    return user


async def delete_user(user_id: int) -> None:
    async with AsyncSession(engine) as session:
        user: User | None = await _get_user(session, user_id)
        await session.delete(user)
        await session.commit()
