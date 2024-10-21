import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.admins_panel import router_admin
from app.handlers import router
from app.functions import create_db
from config import TOKEN

# load_dotenv()
# ADMINS = os.getenv('ADMIN_ID')
# TOKEN = os.getenv('TOKEN') # не робит
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(router, router_admin)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(create_db())
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
