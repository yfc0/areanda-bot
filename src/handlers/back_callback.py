from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters.command import Command

from keyboards.inline import get_main_menu_k

from .main_message import main_menu

import logging

logger = logging.getLogger(__name__)

router = Router()

@router.callback_query(F.data == "back_main_menu")
async def back_main_menu(callback: CallbackQuery, session, state: FSMContext):
    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    await callback.message.delete()
    await main_menu(callback.message, session, state, callback.from_user.id)
