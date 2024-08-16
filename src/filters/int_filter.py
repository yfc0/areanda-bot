from aiogram.filters import BaseFilter
from aiogram.types import Message


class IntFilter(BaseFilter):
    '''Проверяет является ли строка целым, положительным числом, больше нуля'''

    async def __call__(self, message: Message) -> bool:
        if not message.text.isdigit():
            await message.answer(text="Введите целое, положительное число")
            return False
        if int(message.text) == 0:
            await message.answer(text="Число должно быть больше нуля")
            return False
        return True
