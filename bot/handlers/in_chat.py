from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.filters import IsAdminFilter
from bot.states import AdminStates
from config import config

router = Router()
router.message.filter(IsAdminFilter(config.ADMIN), StateFilter(AdminStates.in_chat))


@router.message(Command("cancel", "exit", "stop"), StateFilter(AdminStates.in_chat))
async def cancel_chat_cmd(message: Message, state: FSMContext):
    user_id: int = (await state.get_data())["user_id"]
    await state.clear()
    await message.answer(f"Чат с {user_id} закончен...")


@router.message(StateFilter(AdminStates.in_chat))
async def echo(message: Message, state: FSMContext) -> None:
    user_id: int = (await state.get_data())["user_id"]
    await message.answer(f'Передаю сообщение "{message.text}" -> {user_id}...')
