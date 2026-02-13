from aiogram import Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.db import read_user
from bot.db.models import User
from bot.filters import IsAdminFilter
from bot.states import AdminStates
from config import config

router = Router()
router.message.filter(IsAdminFilter(config.ADMIN))


@router.message(Command("chat"), StateFilter(None))
async def start_chat_cmd(
    message: Message, command: CommandObject, state: FSMContext
) -> None:
    args: str | None = command.args
    if not args:
        await message.answer("Укажи аргументы...")
        return
    if not args.isdigit():
        await message.answer("id должен состоять из цифр...")
        return
    user_id = int(args)
    user: User | None = await read_user(user_id)
    if not user:
        await message.answer("Пользователь с таким id не найден...")
        return
    await state.set_state(AdminStates.in_chat)
    await state.set_data({"user_id": user_id})
    await message.answer(f"Чат с {user.name} {user.user_id} установлен...")


@router.message(Command("status"))
async def status_cmd(message: Message, state: FSMContext) -> None:
    if await state.get_state() is None:
        await message.reply("Сейчас не в чате")
        return
    await message.reply(f"Сейчас в чате с {(await state.get_data())['user_id']}")
