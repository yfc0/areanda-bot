from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import any_state

import logging

from keyboards.inline import get_admin_menu_k, get_accept_cancel_k

from states.states import AdminMenu, CreateProduct

from middleware.admin import IsAdminMiddleware

from services.admin import AdminService

from filters.int_filter import IntFilter

router = Router()


async def _admin_menu(message: Message, session, state: FSMContext, edit=False):

    await state.clear()
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
    if edit:
        await message.edit_text(text=text_menu, reply_markup=get_admin_menu_k())
        return
    await message.answer(text=text_menu, reply_markup=get_admin_menu_k())


@router.message(Command("admin"))
async def admin_menu(message: Message, session, state: FSMContext):
    '''Админ меню'''
    logging.info("handler admin menu")
    await _admin_menu(message, session, state)


@router.message(Command("state"))
async def current_state(message: Message, state: FSMContext):
    await message.answer(text=f"STATE: {await state.get_state()}\n\nDATA: {await state.get_data()}")


@router.message(F.text, StateFilter(AdminMenu.category_name))
async def get_category_name(message: Message, state: FSMContext):
    '''Получить имя категории'''

    logging.info("handler get name")
    await state.update_data(name=message.text)
    await message.answer(text=f"Вы ввели {message.text}\nЧтобы сменить название введите его повторно",
                                   reply_markup=get_accept_cancel_k())


@router.message(F.text, StateFilter(AdminMenu.del_category), IntFilter())
async def get_category_id(message: Message, state: FSMContext):
    '''Получить id категории'''

    logging.info("handler get category id")
    category_id = int(message.text)
    await state.update_data(category=category_id)
    await message.answer(text=f"Вы ввели {message.text}\nЧтобы сменить id введите его повторно",
                                   reply_markup=get_accept_cancel_k())


@router.message(F.text, StateFilter(AdminMenu.del_product), IntFilter())
async def get_product_id(message: Message, state: FSMContext):
    '''Получить id товара'''

    logging.info("handler get product id")
    product_id = int(message.text)
    await state.update_data(product=product_id)
    await message.answer(text=f"Вы ввели {message.text}\nЧтобы сменить id введите его повторно",
                                   reply_markup=get_accept_cancel_k())


@router.message(F.text, StateFilter(CreateProduct.name))
async def get_product_name(message: Message, state: FSMContext):
    '''Получить имя товара'''

    logging.info("handler get_product name")
    await state.update_data(product_name=message.text)
    await message.answer(text=f"Вы ввели {message.text}\nЧтобы сменить имя введите его повторно",
                         reply_markup=get_accept_cancel_k())


@router.message(F.text, StateFilter(CreateProduct.description))
async def get_product_description(message: Message, state: FSMContext):
    '''Получить описание товара'''

    logging.info("handler get product description")
    await state.update_data(product_description=message.text)
    await message.answer(text=f"Вы ввели {message.text}\nЧтобы сменить имя введите его повторно",
                         reply_markup=get_accept_cancel_k())


@router.message(F.photo, StateFilter(CreateProduct.photo))
async def get_product_photo(message: Message, state: FSMContext):
    '''Получить фото товара'''

    logging.info("handler get product photo")
    photo = message.photo[0].file_id
    await state.update_data(photo=photo)
    await message.answer_photo(caption="Чтобы сменить фото отправьте его повторно", photo=photo,
                         reply_markup=get_accept_cancel_k())
