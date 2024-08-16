import os
import asyncio
import logging
from logging.config import fileConfig

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from handlers.user_router import user_router
from handlers.admin_router import admin_router

from db.db import init_db

from redis.asyncio.client import Redis

from middleware.session import SessionMiddleware

from utils.logging import Logger


Logger.setup()
fileConfig("/etc/logging_config.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


API_TOKEN = os.getenv("TOKEN")
bot = Bot(token=API_TOKEN)


async def main():
    await init_db()

    storage = RedisStorage.from_url(os.getenv("REDIS_URL"))

    dp = Dispatcher(storage=storage)
    dp.update.middleware(SessionMiddleware())
    dp.include_router(admin_router)
    dp.include_router(user_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("start bot")
    asyncio.run(main())
