import logging
from app.logger.setup_logger import setup_logging

from aiogram import Bot
from app.bot import dp, bot, set_commands
from app.handlers import welcome_handler, get_vpn
from app.handlers import menu_handler

import asyncio



async def main():
   setup_logging()

   logger = logging.getLogger()

   await set_commands(bot)

   dp.include_routers(welcome_handler.router, menu_handler.router, get_vpn.router)

   try:
       logger.info("starting bot")

       await dp.start_polling(bot)
   except Exception as e:
       logger.error(f"Error in main: {e}")
   finally:
       if bot and isinstance(bot, Bot):
          await bot.session.close()





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
