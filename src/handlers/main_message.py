from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command

import logging

from keyboards.inline import get_main_menu_k
from keyboards.reply import get_contact_k

from .get_rent_callback import router as get_rent_router

from services import auth


router = Router()
router.include_router(get_rent_router)


@router.message(Command("start", "menu"))
async def start(message: Message, session):
    '''Главное меню'''
    logging.info("handler start")
    if not await auth.check(session, message.from_user.id):
        await message.answer(text="need reg")
        return
    menu_text= f"Жизни: ❤️❤️💔\nВаш tg id: `{message.from_user.id}`"
    await message.answer(text=menu_text, reply_markup=get_main_menu_k(),
                         parse_mode="MarkDownV2")
