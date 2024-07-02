from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import any_state

import logging

from keyboards.inline import get_admin_menu_k, get_accept_cancel_k

from states.states import AdminMenu

from middleware.admin import IsAdminMiddleware

from services.admin import AdminService

from .utils import check_literal_int

router = Router()

@router.message(Command("admin"))
async def admin_menu(message: Message, session):
    '''Админ меню'''

    logging.info("handler admin menu")
    text_menu = '''
Меню администратора.

Ниже описан функционал доступный администратору
|
v

Раздел Категории:
Создать и удалить категорию

Раздел Товары:
Создать и удалить товар.

Раздел Аренда:
Принять или отклонить заявку на взятие, или сдачу, товара в аренду.

Раздел Пользователи:
Информация о юзерах, корректировка сердец.
    '''
    await message.answer(text=text_menu, reply_markup=get_admin_menu_k())


@router.message(F.text, StateFilter(AdminMenu.category_name))
async def get_name(message: Message, state: FSMContext):
    logging.info("handler get name")
    await state.update_data(name=message.text)
    await message.answer(text=f"Вы ввели {message.text}\nЧтобы сменить название введите его повторно",
                                   reply_markup=get_accept_cancel_k())


@router.message(F.text, StateFilter(AdminMenu.del_category))
async def get_category_id(message: Message, state: FSMContext):
    logging.info("handler get category id")
    if not check_literal_int(message.text):
        await message.answer(text="Введите число")
        return
    category_id = int(message.text)
    await state.update_data(category=category_id)
    await message.answer(text=f"Вы ввели {message.text}\nЧтобы сменить id введите его повторно",
                                   reply_markup=get_accept_cancel_k())
