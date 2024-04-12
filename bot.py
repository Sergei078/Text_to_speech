import asyncio
from aiogram import Bot, Dispatcher
from handlers import router
import logging
import os
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


async def start_bot():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(start_bot())
    except Exception as e:
        logging.error(str(e))
