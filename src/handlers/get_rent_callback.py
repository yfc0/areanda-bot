from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters.command import Command

from keyboards.inline import get_menu_get_rent_k

import logging

router = Router()

@router.callback_query(F.data == "get_rent")
async def get_rent(callback: CallbackQuery):
    logging.info("handler get_rent")
    menu_text = "Выберите категорию товара"
    await callback.message.edit_text(text=menu_text, reply_markup=get_menu_get_rent_k())
