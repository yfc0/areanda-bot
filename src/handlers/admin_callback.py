from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from services.admin import AdminService

from states.states import AdminMenu, CreateProduct

from keyboards.inline import get_categories_menu_am_k, get_products_menu_am_k, get_categories_list_am_k, \
                             get_accept_cancel_k
from keyboards.pagination import Paginator

from services.admin import AdminService

import logging

from .admin_message import _admin_menu

logger = logging.getLogger(__name__)

router = Router()


async def _categories_menu(callback: CallbackQuery, session, state: FSMContext):
    ids_list = await AdminService(session).ids_list_category()
    paginator = Paginator(ids_list, 5)
    await state.update_data(paginator=vars(paginator))
    categories = await AdminService(session).category_list_text(paginator.current_page)
    await callback.message.edit_text(text=f"Список категорий:\n\n{categories}",
                                             reply_markup=get_categories_menu_am_k(paginator))


@router.callback_query(F.data == "categories_am")
async def categories_menu(callback: CallbackQuery, session, state: FSMContext):
    '''Меню раздела категории'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    await _categories_menu(callback, session, state)


@router.callback_query(lambda callback: callback.data in ["back_page", "next_page"])
async def paginate_category(callback: CallbackQuery, state: FSMContext, session):
    '''Пагинация категорий'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    data = await state.get_data()
    paginator = Paginator(**data['paginator'])
    if callback.data == "back_page":
        paginator.back()
    if callback.data == "next_page":
        paginator.next()
    await state.update_data(paginator=vars(paginator))
    categories = await AdminService(session).category_list_text(paginator.current_page)
    await callback.message.edit_text(text=f"Список категорий:\n\n{categories}",
                                             reply_markup=get_categories_menu_am_k(paginator))


@router.callback_query(F.data == "create_category")
async def create_category(callback: CallbackQuery, state: FSMContext):
    '''Создание категории'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    await callback.message.delete()
    await state.set_state(AdminMenu.category_name)
    await callback.message.answer(text="Введите название категории")


@router.callback_query(F.data == "del_category")
async def del_category(callback: CallbackQuery, state: FSMContext):
    '''Удаление категории'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    await callback.message.delete()
    await state.set_state(AdminMenu.del_category)
    await callback.message.answer(text="Введите id категории, чтобы удалить ее.")


@router.callback_query(F.data == "accept", StateFilter(AdminMenu.del_category))
async def accept_del_category(callback: CallbackQuery, session, state: FSMContext):
    '''Удалить категорию'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    data = await state.get_data()
    await AdminService(session).delete_category(id=data["category"])
    await state.clear()
    await _categories_menu(callback, session, state)


@router.callback_query(F.data == "accept", StateFilter(AdminMenu.category_name))
async def save_category(callback: CallbackQuery, session, state: FSMContext):
    '''Сохранить категорию'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    data = await state.get_data()
    await AdminService(session).save_category(name=data["name"])
    await state.clear()
    await _categories_menu(callback, session, state)


async def _products_menu(callback: CallbackQuery, session, state: FSMContext, with_image=False):
    products = await AdminService(session).products_list()
    if with_image:
        await callback.message.delete()
        await callback.message.answer(text=f"{products}",
                                 reply_markup=get_products_menu_am_k())
        return
    await callback.message.edit_text(text=f"{products}",
                                 reply_markup=get_products_menu_am_k())


@router.callback_query(F.data == "products_am")
async def products_menu(callback: CallbackQuery, session, state: FSMContext):
    '''Меню раздела товары'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    await _products_menu(callback, session, state)


@router.callback_query(F.data == "create_product")
async def create_product(callback: CallbackQuery, session, state: FSMContext):
    '''Создание продукта'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    await state.set_state(CreateProduct.name)
    await callback.message.edit_text(text="Введите имя товара")


@router.callback_query(F.data == "accept", StateFilter(CreateProduct.name))
async def accept_product_name(callback: CallbackQuery, session, state: FSMContext):
    '''Принять название товара'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    await state.set_state(CreateProduct.description)
    await callback.message.edit_text(text="Введите описание товара")


@router.callback_query(F.data == "accept", StateFilter(CreateProduct.description))
async def accept_product_description(callback: CallbackQuery, session, state: FSMContext):
    '''Принять описание товара'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    await state.set_state(CreateProduct.photo)
    await callback.message.edit_text(text="Отправьте фото товара")


@router.callback_query(F.data == "accept", StateFilter(CreateProduct.photo))
async def accept_product_photo(callback: CallbackQuery, session, state: FSMContext):
    '''Принять фото товара'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    await state.set_state(CreateProduct.category)
    ids_list = await AdminService(session).ids_list_category()
    paginator = Paginator(ids_list, 5)
    await state.update_data(paginator=vars(paginator))
    categories = await AdminService(session).category_list(paginator.current_page)
    await callback.message.delete()
    await callback.message.answer(text="Выберите категорию",
                                     reply_markup=get_categories_list_am_k(paginator, categories))


@router.callback_query(StateFilter(CreateProduct.category), lambda callback: callback.data in ["back_page_cl", "next_page_cl"])
async def paginate_category_list(callback: CallbackQuery, session, state: FSMContext):
    '''Пагинация категорий'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    data = await state.get_data()
    paginator = Paginator(**data['paginator'])
    if callback.data == "back_page_cl":
        paginator.back()
    if callback.data == "next_page_cl":
        paginator.next()
    await state.update_data(paginator=vars(paginator))
    categories = await AdminService(session).category_list(paginator.current_page)
    text = ""
    if "product_category" in data:
        category = await AdminService(session).category_name(data['product_category'])
        text += f"Вы выбрали {category}\n\nВыберите повторно, чтобы изменить"
        await callback.message.edit_text(text=text, reply_markup=get_categories_list_am_k(paginator, categories,
                                                                                          True))
        return
    else:
        text += "Выберите категорию"
    await callback.message.edit_text(text=text, reply_markup=get_categories_list_am_k(paginator, categories))


@router.callback_query(F.data.startswith("category_id_"), StateFilter(CreateProduct.category))
async def get_product_category(callback: CallbackQuery, session, state: FSMContext):
    '''Получить категорию товара'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    data = await state.get_data()
    paginator = Paginator(**data['paginator'])
    category_id = int(callback.data.split("category_id_")[1])
    await state.update_data(product_category=category_id)
    category = await AdminService(session).category_name(category_id)
    categories = await AdminService(session).category_list(paginator.current_page)
    await callback.message.edit_text(text=f"Вы выбрали {category}\n\nВыберите повторно, чтобы изменить",
                                     reply_markup=get_categories_list_am_k(paginator, categories, True))


@router.callback_query(F.data == "accept", StateFilter(CreateProduct.category))
async def accept_product_category(callback: CallbackQuery, session, state: FSMContext):
    '''Принять категорию для товара'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    await state.set_state(CreateProduct.end)
    data = await state.get_data()
    category = await AdminService(session).category_name(data['product_category'])
    text = f"Завершите создание товара\n\nИмя товара: {data['product_name']}\nОписание: {data['product_description']}\nКатегория: {category}"
    await callback.message.delete()
    await callback.message.answer_photo(caption=text, photo=data['photo'], reply_markup=get_accept_cancel_k())


@router.callback_query(F.data == "accept", StateFilter(CreateProduct.end))
async def end_create_product(callback: CallbackQuery, session, state: FSMContext):
    '''Закончить создание товара'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    data = await state.get_data()
    await AdminService(session).save_product(data['product_name'], data['product_description'],
                                             data['photo'], data['product_category'], callback.from_user.id)
    await _products_menu(callback, session, state, True)


@router.callback_query(F.data == "del_product")
async def del_product(callback: CallbackQuery, session, state: FSMContext):
    '''Удаление товара'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    await state.set_state(AdminMenu.del_product)
    await callback.message.edit_text(text="Введите id товара, чтобы удалить ее.")


@router.callback_query(F.data == "accept", StateFilter(AdminMenu.del_product))
async def accept_del_product(callback: CallbackQuery, session, state: FSMContext):
    '''Удалить категорию'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    data = await state.get_data()
    await AdminService(session).delete_product(id=data["product"])
    await state.clear()
    await _products_menu(callback, session, state)


@router.callback_query(F.data == "back")
async def back_menu(callback: CallbackQuery, session, state: FSMContext):

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    await _admin_menu(callback.message, session, state, True)
