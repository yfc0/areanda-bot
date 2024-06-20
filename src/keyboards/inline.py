from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu_k():
    builder = InlineKeyboardBuilder()
    builder.button(text="Взять в аренду", callback_data="get_rent")
    builder.button(text="Сдать в аренду", callback_data="pass_rent")
    builder.button(text="Мои заявки", callback_data="my_applications")
    builder.button(text="Помощь", callback_data="help")
    builder.adjust(1)
    return builder.as_markup()
