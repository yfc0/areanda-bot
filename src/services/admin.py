from db.models import Category, Product

from sqlalchemy import select


class AdminService:
    def __init__(self, session):
        self.session = session


    async def save_category(self, name):
        '''Создание категории товара'''
        category = Category(name=name)
        self.session.add(category)


    async def category_list(self):
        '''Список категорий по id и name'''
        categories = await self._category_list()
        if not categories:
            return "нет созданных категорий"
        category_list = ""
        for category in categories:
            category_list += f"ID: {category.id} | {category.name}\n"
        return category_list


    async def _category_list(self):
        '''Все категории'''
        query = select(Category)
        categories = await self.session.execute(query)
        return categories.scalars().all()


    async def delete_category(self, id):
        '''Удалить категорию'''
        query = select(Category).where(id==id)
        category = await self.session.scalar(query)
        await self.session.delete(category)
