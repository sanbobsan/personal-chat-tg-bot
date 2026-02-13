from aiogram import Router

from .start import router as start_router
from .admin import router as admin_router
from .in_chat import router as in_chat_router

main_router = Router()
main_router.include_routers(start_router, admin_router, in_chat_router)


__all__ = [
    "main_router",
]
