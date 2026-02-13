from aiogram import Router

from bot.middlewares import AdminOrEchoMiddleware
from config import config

from .admin import router as admin_router
from .in_chat import router as in_chat_router
from .start import router as start_router

admin_router.include_router(in_chat_router)

admin_or_echo_router = Router()
admin_or_echo_router.message.outer_middleware(AdminOrEchoMiddleware(config.ADMIN))
admin_or_echo_router.include_router(admin_router)

main_router = Router()
main_router.include_routers(start_router, admin_or_echo_router)


__all__ = [
    "main_router",
]
