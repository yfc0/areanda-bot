from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu_k():
    builder = InlineKeyboardBuilder()
    builder.button(text="Взять в аренду", callback_data="get_rent")
    builder.button(text="Сдать в аренду", callback_data="pass_rent")
    builder.button(text="Мои заявки", callback_data="my_applications")
    builder.button(text="Помощь", callback_data="help")
    builder.adjust(1)
    return builder.as_markup()


def get_menu_get_rent_k():
    builder = InlineKeyboardBuilder()
    builder.button(text="Костюмы", callback_data="test")
    builder.button(text="Поиск", callback_data="search")
    builder.button(text="Назад", callback_data="back_main_menu")
    builder.adjust(1)
    return builder.as_markup()


def get_categories_menu_am_k(paginator):
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️", callback_data="back_page")
    builder.button(text=f"{paginator.page_number}/{paginator.number_pages}", callback_data="none")
    builder.button(text="➡️", callback_data="next_page")
    builder.button(text="Создать категорию", callback_data="create_category")
    builder.button(text="Удалить категорию", callback_data="del_category")
    builder.button(text="Назад", callback_data="back")
    builder.adjust(3, 2, 1)
    return builder.as_markup()


def get_categories_list_am_k(paginator, categories, accept_cancel=False):
    builder = InlineKeyboardBuilder()
    if accept_cancel:
        builder.button(text="Принять", callback_data="accept")
        builder.button(text="Отменить", callback_data="cancel")
    builder.button(text="⬅️", callback_data="back_page_cl")
    builder.button(text=f"{paginator.page_number}/{paginator.number_pages}", callback_data="none")
    builder.button(text="➡️", callback_data="next_page_cl")
    for category in categories:
        builder.button(text=f"{category.name}", callback_data=f"category_id_{category.id}")
    if accept_cancel:
        builder.adjust(2, 3, 1)
    else:
        builder.adjust(3, 1)
    return builder.as_markup()


def get_products_menu_am_k():
    builder = InlineKeyboardBuilder()
    builder.button(text="Добавить товар", callback_data="create_product")
    builder.button(text="Удалить товар", callback_data="del_product")
    builder.button(text="Назад", callback_data="back")
    builder.adjust(2)
    return builder.as_markup()

def get_admin_menu_k():
    builder = InlineKeyboardBuilder()

   # am in callback data this admin menu
    builder.button(text="Категории", callback_data="categories_am")
    builder.button(text="Товары", callback_data="products_am")
    builder.button(text="Аренда", callback_data="rent_am")
    builder.button(text="Пользователи", callback_data="users_am")
    builder.adjust(1)
    return builder.as_markup()


def get_accept_cancel_k():
    builder = InlineKeyboardBuilder()
    builder.button(text="Принять", callback_data="accept")
    builder.button(text="Отменить", callback_data="cancel")
    builder.adjust(2)
    return builder.as_markup()
