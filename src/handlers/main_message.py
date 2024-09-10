from aiogram import F
from aiogram.types import Message
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import any_state

import logging

from keyboards.inline import get_main_menu_k
from keyboards.reply import get_contact_k

from states.states import Registration

from services import auth
from services.user import UserService
from aiogram import Router

logger = logging.getLogger(__name__)

router = Router()


heart = "❤️"


async def main_menu(message: Message, session, state: FSMContext, user_id):
    user_hearts = await UserService(session).count_heart(user_id)
    menu_text= f"Жизни: {heart * user_hearts} {user_hearts}/3\nВаш tg id: `{user_id}`"
    await message.answer(text=menu_text, reply_markup=get_main_menu_k(),
                         parse_mode="MarkDownV2")


@router.message(Command("start", "menu"))
async def start(message: Message, session, state: FSMContext):
    '''Регистрация и главное меню'''

    logger.info(f"user: {message.from_user.id} state: {await state.get_state()}")
    await state.clear()
    user_id = message.from_user.id
    if not await auth.check(session, user_id):
        await state.set_state(Registration.contact_data)
        await message.answer(text="Пройдите регистрацию")
        await message.answer(text="Отправьте номер телефона", reply_markup=get_contact_k())
        return
    await main_menu(message, session, state, user_id)


@router.message(F.contact, StateFilter(Registration.contact_data))
async def get_contact_data(message: Message, session, state: FSMContext):
    '''Получить контактные данные'''

    logger.info(f"user: {message.from_user.id} state: {await state.get_state()}")
    tg_id = message.contact.user_id
    first_name = message.contact.first_name
    last_name = message.contact.last_name
    phone_number = message.contact.phone_number
    await UserService(session).create(id=tg_id, first_name=first_name, last_name=last_name,
                                      phone_number=phone_number)
    await state.clear()
    await message.answer(text="Вы прошли регистрацию", reply_markup=ReplyKeyboardRemove())
    await start(message, session, state)
