from db.models import User

from sqlalchemy import select


class UserService:
    def __init__(self, session):
        self.session = session


    async def get_by_id(self, id):
        query = select(User).where(User.id == id)
        user = await self.session.scalar(query)
        return user


    async def create(self, id, first_name, last_name, phone_number, username=None):
       user = User(id=id, first_name=first_name, last_name=last_name, username=username,
                   phone_number=phone_number)
       self.session.add(user)