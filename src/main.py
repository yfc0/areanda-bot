import os
import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import main_message
from handlers import admin_message

from db.db import init_db

from middleware.session import SessionMiddleware


API_TOKEN = os.getenv("TOKEN")
bot = Bot(token=API_TOKEN)

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%H:%M:%S")


async def main():
    await init_db()

    dp = Dispatcher()
    dp.update.middleware(SessionMiddleware())
    dp.include_router(main_message.router)
    dp.include_router(admin_message.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.info("start bot")
    asyncio.run(main())
