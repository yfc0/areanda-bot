from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_contact_k():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Отправить номер телефона",
                   request_contact=True)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
