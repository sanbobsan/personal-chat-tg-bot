import asyncio
import logging
from asyncio.exceptions import CancelledError

from bot.create_bot import bot, dp
from bot.db import init_models
from bot.handlers import main_router


async def main() -> None:
    try:
        await init_models()
        dp.include_router(main_router)
        await bot.delete_webhook()
        await dp.start_polling(bot)

    except (KeyboardInterrupt, CancelledError):
        logging.info("Bot turned off by cancel")

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
