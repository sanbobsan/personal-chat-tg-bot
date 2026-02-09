from aiogram.filters import Filter
from aiogram.types import Message


class IsAdminFilter(Filter):
    def __init__(self, admin_id: int) -> None:
        self.admin_id: int = admin_id

    async def __call__(self, message: Message) -> bool:
        if not message.from_user:
            return False
        return message.from_user.id == self.admin_id
