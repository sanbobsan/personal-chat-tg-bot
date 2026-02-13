from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.create_bot import bot
from bot.db import read_user
from bot.db.models import User
from bot.filters import IsAdminFilter
from bot.states import AdminStates
from config import config

router = Router()
router.message.filter(IsAdminFilter(config.ADMIN), StateFilter(AdminStates.in_chat))


async def _get_user(state: FSMContext):
    user_id: int = (await state.get_data())["user_id"]
    user: User | None = await read_user(user_id)
    return user


@router.message(Command("cancel", "exit", "stop"), StateFilter(AdminStates.in_chat))
async def cancel_chat_cmd(message: Message, state: FSMContext):
    user: User | None = await _get_user(state)
    await state.clear()
    if not user:
        return
    await message.answer(f"Чат с {user.name} {user.user_id} закончен...")


@router.message(StateFilter(AdminStates.in_chat))
async def echo(message: Message, state: FSMContext) -> None:
    user: User | None = await _get_user(state)
    if not user:
        await message.answer(
            f"Не удалось передать сообщение, такого пользователя не существует... ({(await state.get_data())['user_id']})"
        )
        return
    text: str | None = message.text
    if not text:
        return
    await bot.send_message(user.user_id, text=text)
