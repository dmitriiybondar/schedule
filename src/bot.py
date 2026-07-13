import os
import sys
import asyncio
import logging 
import database.models # НЕ ВИДАЛЯТИ

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram import F

from database.connection import engine, Base
from handlers.user import router as user_router
from handlers.commands import router as command_router
from handlers.schedule import router as schedule_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    load_dotenv()

    await init_db()

    admin = int(os.getenv("ADMIN_USER_ID"))
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.message.filter(F.from_user.id == admin)
    dp.callback_query.filter(F.from_user.id == admin)

    dp.include_router(user_router)
    dp.include_router(command_router)
    dp.include_router(schedule_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())