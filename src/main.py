import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from handlers.user_router import user_router
from handlers.admin_router import admin_router

from db.db import init_db

from redis.asyncio.client import Redis

from middleware.session import SessionMiddleware


API_TOKEN = os.getenv("TOKEN")
bot = Bot(token=API_TOKEN)

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%H:%M:%S")


async def main():
    await init_db()

    storage = RedisStorage.from_url(os.getenv("REDIS_URL"))

    dp = Dispatcher(storage=storage)
    dp.update.middleware(SessionMiddleware())
    dp.include_router(admin_router)
    dp.include_router(user_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.info("start bot")
    asyncio.run(main())
