from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

from app.repository.users import UserRepository


class CheckUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id

        if UserRepository.exists(user_id):
            await event.answer("Ты уже получал VPN-конфиг ✅")
            return
        return await handler(event, data)