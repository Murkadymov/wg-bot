# from typing import Union, Dict, Any
#
# from aiogram.types import Message
#
# class InstructionFilter:
#     async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
#         text = message.text or ""
#         # Условие: либо кнопка, либо команда
#         if text == "Инструкция" or text.startswith("/instruction"):
#             return True
#         return False