from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.create_bot import bot
from bot.db import read_user
from bot.db.models import User


class AdminOrEchoMiddleware(BaseMiddleware):
    def __init__(self, admin_id: int) -> None:
        self.admin_id: int = admin_id

    async def __call__(self, handler, event, data) -> None | Any:
        if not isinstance(event, Message) or not event.from_user or not event.text:
            return None

        if event.from_user.id == self.admin_id:
            result = await handler(event, data)
            return result

        user: User | None = await read_user(event.from_user.id)
        if not user:
            return None

        text: str = f"{user.name} {event.from_user.id} @{event.from_user.username}\n{event.text}"
        await bot.send_message(self.admin_id, text=text)
        return None
