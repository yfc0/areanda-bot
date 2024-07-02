from aiogram import Router

from .main_message import router as main_router
from .get_rent_callback import router as rent_router
from .back_callback import router as back_router

user_router = Router()
user_router.include_router(main_router)
user_router.include_router(rent_router)
user_router.include_router(back_router)
