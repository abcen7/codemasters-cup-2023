from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TELEGRAM_BOT_TOKEN

bot = Bot(TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

if __name__ == "__main__":
    from handlers import *

    executor.start_polling(dp, skip_updates=True)
