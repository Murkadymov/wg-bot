from typing import Union, Dict, Any

from aiogram.types import Message

class InstructionFilter:
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        text = (message.text or "").strip()

        # Разрешаем только точные совпадения
        return text in {"/instruction", "Инструкция"}