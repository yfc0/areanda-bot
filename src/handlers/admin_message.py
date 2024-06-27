from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import any_state

from keyboards.inline import get_admin_menu_k

from middleware.admin import IsAdminMiddleware


router = Router()
router.message.middleware(IsAdminMiddleware())

@router.message(Command("admin"))
async def admin_menu(message: Message, session):
    await message.answer(text="Меню админа", reply_markup=get_admin_menu_k())
