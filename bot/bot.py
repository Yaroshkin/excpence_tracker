import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from handlers import register_handlers 


logging.basicConfig(level=logging.INFO)


bot = Bot(token=TOKEN)


storage = MemoryStorage()


dp = Dispatcher()


register_handlers(dp)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
