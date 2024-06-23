from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters.command import Command

from keyboards.inline import get_main_menu_k

import logging

router = Router()

@router.callback_query(F.data == "back_main_menu")
async def back_main_menu(callback: CallbackQuery):
    logging.info("handler back main menu")
    menu_text= f"Жизни: ❤️❤️💔\nВаш tg id: `{callback.from_user.id}`"
    await callback.message.edit_text(text=menu_text, reply_markup=get_main_menu_k(),
                                     parse_mode="MarkDownV2")
