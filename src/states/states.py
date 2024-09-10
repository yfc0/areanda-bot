from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    contact_data = State()


class AdminMenu(StatesGroup):
    category_name = State()
    del_category = State()
    del_product = State()


class Rent(StatesGroup):
    category = State()
    products = State()
    data = State()


class CreateProduct(StatesGroup):
    name = State()
    description = State()
    photo = State()
    category = State()
    end = State()
