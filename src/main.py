import os
import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import main_message

from db.db import init_db


API_TOKEN = os.getenv("TOKEN")
bot = Bot(token=API_TOKEN)


async def main():
    await init_db()

    dp = Dispatcher()
    dp.include_router(main_message.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
