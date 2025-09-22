# from typing import Union, Dict, Any
# from aiogram.filters import BaseFilter
# from aiogram.types import Message
#
# class VPNRequestFilter(BaseFilter):
#     async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
#         text = message.text or ""
#
#         # Условие: либо кнопка, либо команда
#         if text == "Получить VPN" or text.startswith("/getvpn"):
#             return True
#         return False