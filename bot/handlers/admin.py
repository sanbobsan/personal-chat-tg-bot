from aiogram import Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

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
    await state.set_state(AdminStates.in_chat)
    await state.set_data({"user_id": args})
    await message.answer(f"Чат с {args} установлен")


@router.message(Command("status"))
async def status_cmd(message: Message, state: FSMContext) -> None:
    if await state.get_state() is None:
        await message.reply("Сейчас не в чате")
        return
    await message.reply(f"Сейчас в чате с {(await state.get_data())['user_id']}")


@router.message(Command("cancel", "exit", "stop"), StateFilter(AdminStates.in_chat))
async def cancel_chat_cmd(message: Message, state: FSMContext):
    user_id: int = (await state.get_data())["user_id"]
    await state.clear()
    await message.answer(f"Чат с {user_id} закончен...")


@router.message(StateFilter(AdminStates.in_chat))
async def echo(message: Message, state: FSMContext) -> None:
    user_id: int = (await state.get_data())["user_id"]
    await message.answer(f'Передаю сообщение "{message.text}" -> {user_id}...')
