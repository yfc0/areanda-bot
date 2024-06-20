from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command

from keyboards.inline import get_main_menu_k


router = Router()


@router.message(Command("start", "menu"))
async def start(message: Message):
    menu_text= f"Жизни: ❤️❤️💔\nВаш tg id: `{message.from_user.id}`"
    await message.answer(text=menu_text, reply_markup=get_main_menu_k(),
                         parse_mode="MarkDownV2")
