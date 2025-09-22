from typing import Callable, Dict, Any, Awaitable, Union
from aiogram.types import Message, CallbackQuery
from aiogram import BaseMiddleware
from app.repository.users import UserRepository

Event = Union[Message, CallbackQuery]

class CheckUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Event, Dict[str, Any]], Awaitable[Any]],
        event: Event,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        if UserRepository.exists(user_id):
            text = "Ты уже получал VPN-конфиг ✅"
            if isinstance(event, CallbackQuery):
                await event.answer(text, show_alert=False)
            else:
                await event.answer(text)
            return
        return await handler(event, data)
