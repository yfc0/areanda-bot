from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from keyboards.inline import get_menu_get_rent_k

from services.admin import AdminService
from services.product import ProductService

from keyboards.pagination import Paginator
from keyboards.inline import get_categories_list_am_k, get_products_with_basket, add_main_menu_b

from states.states import Rent

import logging

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == "get_rent")
async def get_rent(callback: CallbackQuery, session, state: FSMContext):
    '''Взять товар в аренду'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    await state.set_state(Rent.category)
    ids_list = await AdminService(session).ids_list_category()
    paginator = Paginator(ids_list, 5)
    await state.update_data(paginator=vars(paginator))
    categories = await AdminService(session).category_list(paginator.current_page)
    keyboard = add_main_menu_b(get_categories_list_am_k(paginator, categories))
    await callback.message.edit_text(text="Выберите категорию", reply_markup=keyboard)


@router.callback_query(StateFilter(Rent.category), lambda callback: callback.data in ["back_page_cl", "next_page_cl"])
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
    await callback.message.edit_text(text="Выберите категорию",
                                     reply_markup=get_categories_list_am_k(paginator, categories))


@router.callback_query(StateFilter(Rent.category), F.data.startswith("category_id_"))
async def get_category(callback: CallbackQuery, session, state: FSMContext, basket):
    '''Получить категорию'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()}")
    category_id = int(callback.data.split("category_id_")[1])
    ids_list = await AdminService(session).products_ids_list_category(category_id)
    if not ids_list:
        await callback.answer(text="В данной категории нет товара", alert_show=True)
        return
    paginator = Paginator(ids_list, 1)
    product = await AdminService(session).get_product(*paginator.current_page)
    await state.update_data(paginator=vars(paginator))
    await state.set_state(Rent.products)
    await callback.message.delete()
    keyboard = add_main_menu_b(get_products_with_basket(paginator, basket))
    await callback.message.answer_photo(caption=ProductService.description(product), photo=product.photo,
                                        reply_markup=keyboard)


@router.callback_query(StateFilter(Rent.products), F.data.startswith("in_basket_"))
async def in_basket(callback: CallbackQuery, session, state: FSMContext, basket):
    '''Если товара нет, то добавить его, иначе удалить'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()} basket: {basket.items}")
    data = await state.get_data()
    paginator = Paginator(**data["paginator"])
    product_id = int(callback.data.split("in_basket_")[1])
    product = await AdminService(session).get_product(product_id)
    keyboard = add_main_menu_b(get_products_with_basket(paginator, basket))
    if basket.check_product(product_id):
       basket.remove(product_id)
       await callback.message.edit_reply_markup(reply_markup=keyboard)
    else:
        basket.add(product.id, product.name)
        await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(StateFilter(Rent.products), lambda callback: callback.data in ["back_page_pb", "next_page_pb"])
async def paginate_product_list(callback: CallbackQuery, session, state: FSMContext, basket):
    '''Пагинация товара'''

    logger.info(f"user: {callback.from_user.id} state: {await state.get_state()} basket: {basket.items}")
    data = await state.get_data()
    paginator = Paginator(**data['paginator'])
    if callback.data == "back_page_pb":
        paginator.back()
    if callback.data == "next_page_pb":
        paginator.next()
    await state.update_data(paginator=vars(paginator))
    product = await AdminService(session).get_product(*paginator.current_page)
    keyboard = add_main_menu_b(get_products_with_basket(paginator, basket))
    photo = InputMediaPhoto(media=product.photo, caption=ProductService.description(product))
    await callback.message.edit_media(media=photo, reply_markup=keyboard)
