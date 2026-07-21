import os
import sys
import asyncio
import logging 

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram import F

from src.database import models # НЕ ВИДАЛЯТИ
from src.database.connection import engine, Base
from src.handlers.user import router as user_router
from src.handlers.host import router as host_router
from src.handlers.commands import router as command_router
from src.handlers.schedule import router as schedule_router

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
admin = int(os.getenv("ADMIN_USER_ID"))

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await init_db()

    dp = Dispatcher()

    dp.message.filter(F.from_user.id == admin)
    dp.callback_query.filter(F.from_user.id == admin)

    dp.include_router(user_router)
    dp.include_router(host_router)
    dp.include_router(command_router)
    dp.include_router(schedule_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())