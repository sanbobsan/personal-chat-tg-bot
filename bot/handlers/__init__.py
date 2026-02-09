from aiogram import Router

from .start import router as start_router
from .admin import router as admin_router

main_router = Router()
main_router.include_routers(start_router, admin_router)


__all__ = [
    "main_router",
]
