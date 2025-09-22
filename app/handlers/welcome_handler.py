from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboards.welcome_buttons import welcome_menu_keyboard
from app.logger.setup_logger import get_logger

logger = get_logger(__name__)

router = Router()

@router.message(Command("start"))
async def start(message: types.Message) -> None:
    logger.info("received start command")

    keyboard = welcome_menu_keyboard()



    await message.answer("Добро пожаловать!\n"
                         "Нажмите на кнопку раздела 'Меню', чтобы открыть меню навигации",
                         reply_markup=keyboard)
    logger.info("reply sent to start command")
