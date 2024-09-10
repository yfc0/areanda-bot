from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_contact_k():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Отправить номер телефона",
                   request_contact=True)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def main_menu_k():
    builder = ReplyKeyboardBuilder()
    builder.button(text="В главное меню", is_persistent=True, resize_keyboard=True)
