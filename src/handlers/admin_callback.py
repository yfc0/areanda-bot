from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from services.admin import AdminService

from states.states import AdminMenu

from keyboards.inline import get_categories_menu_am_k

from services.admin import AdminService

import logging

from .admin_message import admin_menu

router = Router()


@router.callback_query(F.data == "categories_am")
async def categories_menu(callback: CallbackQuery, session):
    '''Меню раздела категории'''

    logging.info("categories menu handler")
    categories = await AdminService(session).category_list()
    await callback.message.edit_text(text=f"Список категорий:\n{categories}",
                                             reply_markup=get_categories_menu_am_k())


@router.callback_query(F.data == "create_category")
async def create_category(callback: CallbackQuery, state: FSMContext):
    '''Создание категории'''
    logging.info("handler callback create category")
    await callback.message.delete()
    await state.set_state(AdminMenu.category_name)
    await callback.message.answer(text="Введите название категории")


@router.callback_query(F.data == "del_category")
async def del_category(callback: CallbackQuery, state: FSMContext):
    logging.info("handler del category")
    await callback.message.delete()
    await state.set_state(AdminMenu.del_category)
    await callback.message.answer(text="Введите id категории, чтобы удалить ее.")


@router.callback_query(F.data == "accept", StateFilter(AdminMenu.del_category))
async def accept_del(callback: CallbackQuery, session, state: FSMContext):
    logging.info("handler accept_del")
    data = await state.get_data()
    await AdminService(session).delete_category(id=data["category"])
    await state.clear()
    await categories_menu(callback, session)


@router.callback_query(F.data == "accept", StateFilter(AdminMenu.category_name))
async def save_category(callback: CallbackQuery, session, state: FSMContext):
    '''Сохранить категорию'''
    logging.info("handler save category")
    data = await state.get_data()
    await AdminService(session).save_category(name=data["name"])
    await state.clear()
    await categories_menu(callback, session)


@router.callback_query(F.data == "back")
async def back_menu(callback: CallbackQuery, session):
    await callback.message.delete()
    await admin_menu(callback.message, session)
