from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.middlewares.host import HostCheckMiddleware
from src.database.connection import AsyncSessionLocal


router = Router()
router.message.middleware(HostCheckMiddleware(session_pool=AsyncSessionLocal))

@router.message(Command("setup_schedule"))
async def setup_chedule(message: Message):
    button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Відкрити розклад",
            web_app=WebAppInfo(url="https://uncrystallized-daisey-uninterwoven.ngrok-free.dev/admin/dashboard/index.html")
        )]
    ])

    await message.answer("Налаштувати графік", reply_markup=button)