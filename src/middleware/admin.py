from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, Update

from services.user import UserService


class IsAdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        tg_user = data["event_from_user"]
        session = data["session"]
        role = await UserService(session).check_role(tg_user.id)
        #if role == "admin":
        if tg_user.id == 314868590:
            return await handler(event, data)
        else:
            return
