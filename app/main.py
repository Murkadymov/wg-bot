import logging
from app.logger.setup_logger import setup_logging

from aiogram import Bot

from app.bot import dp, bot, set_commands
from app.handlers import welcome_handler, get_vpn, instruction_handler
from app.handlers import menu_handler

import asyncio

from app.middlewares.check_user import CheckUserMiddleware


async def main():
   setup_logging()

   logger = logging.getLogger()

   await set_commands(bot)

   get_vpn.router.message.middleware(CheckUserMiddleware())
   get_vpn.router.callback_query.middleware(CheckUserMiddleware())

   dp.include_routers(welcome_handler.router, menu_handler.router, get_vpn.router, instruction_handler.router)

   try:
       logger.info("starting bot")

       await dp.start_polling(bot)
   except Exception as e:
       logger.error(f"Error in main: {e}")
   finally:
       if bot and isinstance(bot, Bot):
          await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())


