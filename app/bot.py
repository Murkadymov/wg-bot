from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from app.config.config_reader import Settings
from aiogram import Bot, Dispatcher
from app.handlers import welcome_handler, get_vpn
from app.handlers import menu_handler

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/menu", description="Меню"),
        BotCommand(command="/instruction", description="Инструкции"),
        BotCommand(command="/getvpn", description="Получить VPN"),
        BotCommand(command="/help", description="Помощь"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeAllPrivateChats())

token = Settings().bot_token.get_secret_value()

bot = Bot(token=str(token))

dp = Dispatcher()



