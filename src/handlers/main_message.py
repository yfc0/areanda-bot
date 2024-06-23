from aiogram import Router, F
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

from .get_rent_callback import router as get_rent_router

from services import auth
from services.user import UserService


router = Router()
router.include_router(get_rent_router)


@router.message(Command("start", "menu"))
async def start(message: Message, session, state: FSMContext):
    '''Главное меню'''
    logging.info("handler start")
    if not await auth.check(session, message.from_user.id):
        await state.set_state(Registration.contact_data)
        await message.answer(text="Пройдите регистрацию")
        await message.answer(text="Отправьте номер телефона", reply_markup=get_contact_k())
        return
    menu_text= f"Жизни: ❤️❤️💔\nВаш tg id: `{message.from_user.id}`"
    await message.answer(text=menu_text, reply_markup=get_main_menu_k(),
                         parse_mode="MarkDownV2")


@router.message(F.contact, StateFilter(Registration.contact_data))
async def get_contact_data(message: Message, session, state: FSMContext):
    '''Получить контактные данные'''
    tg_id = message.contact.user_id
    first_name = message.contact.first_name
    last_name = message.contact.last_name
    phone_number = message.contact.phone_number
    await UserService(session).create(id=tg_id, first_name=first_name, last_name=last_name,
                                      phone_number=phone_number)
    await message.answer(text="Вы прошли регистрацию", reply_markup=ReplyKeyboardRemove())
    await start(message, session, state)
