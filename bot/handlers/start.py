from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.db import create_user

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    if not message.from_user:
        return
    await message.answer("Bot started")
    await create_user(message.from_user.id, message.from_user.full_name)
