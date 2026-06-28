import os
import sys
import asyncio
import logging 

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram import F

from handlers.base_comands import router as base_commands_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


async def main():
    load_dotenv()

    admin = int(os.getenv("ADMIN_USER_ID"))
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.message.filter(F.from_user.id == admin)
    dp.callback_query.filter(F.from_user.id == admin)

    dp.include_router(base_commands_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())