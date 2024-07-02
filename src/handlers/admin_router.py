from aiogram import Router

from middleware.admin import IsAdminMiddleware

from .admin_callback import router as admin_router_callback
from .admin_message import router as admin_router_message


admin_router = Router()
admin_router.include_router(admin_router_callback)
admin_router.include_router(admin_router_message)
admin_router.message.middleware(IsAdminMiddleware())
admin_router.callback_query.middleware(IsAdminMiddleware())
