from sqlalchemy import select

from .user import UserService


async def check(session, id):
    user = await UserService(session).get_by_id(id)
    if not user:
        return False
    return True
