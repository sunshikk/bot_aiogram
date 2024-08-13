import asyncio
import logging

from aiogram import Bot, Dispatcher
from settings.settings import token
from files.handlers import router

from files import database as db

bot = Bot(token=token)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
