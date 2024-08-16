from db.models import Category, Product

from sqlalchemy import select


class AdminService:
    def __init__(self, session):
        self.session = session


    async def get_category(self, category_id):
        '''Получить категорию по id'''
        query = select(Category).where(Category.id == category_id)
        category = await self.session.scalar(query)
        return category


    async def category_name(self, category_id):
        '''Получить имя категории по id'''
        category = await self.get_category(category_id)
        return category.name


    async def category_list(self, ids_list):
        '''Список категорий по списку ids'''

        query = select(Category).where(Category.id.in_(ids_list))
        categories = await self.session.execute(query)
        return categories.scalars().all()


    async def category_list_text(self, ids_list):
        '''Список категорий в тексте по ids'''

        categories = await self.category_list(ids_list)
        if not categories:
            return "Нет созданных категорий"
        categories_list = ""
        for category in categories:
            categories_list += f"ID: {category.id}| NAME: {category.name}\n"
        return categories_list


    async def ids_list_category(self):
        '''Список ids категорий'''
        query = select(Category.id)
        categories = await self.session.execute(query)
        return categories.scalars().all()


    async def save_category(self, name):
        '''Сохранить категорию'''
        category = Category(name=name)
        self.session.add(category)


    async def delete_category(self, id):
        '''Удалить категорию'''
        query = select(Category).where(id==id)
        category = await self.session.scalar(query)
        await self.session.delete(category)


    async def save_product(self, name, description, photo, category_id):
        '''Сохранить товар'''

        product = Product(name=name, description=description, photo=photo,
                          category_id=category_id)
        self.session.add(product)


    async def delete_product(self, id):
        '''Удалить товар'''

        query = select(Product).where(id==id)
        product = await self.session.scalar(query)
        await self.session.delete(product)


    async def products_list(self):
        '''Список товара по id, name, status'''
        products = await self._products_list()
        if not products:
            return "нет созданных товаров"
        products_list = ""
        for product in products:
            products_list += f"ID: {product.id} | NAME: {product.name} | STATUS: {product.status}\n"
        return products_list


    async def _products_list(self):
        '''Все товары'''
        query = select(Product)
        products = await self.session.execute(query)
        return products.scalars().all()
