from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.middlewares.host import HostCheckMiddleware
from src.database.connection import AsyncSessionLocal
from src.keyboards import setup_schedule_keyboard


router = Router()
router.message.middleware(HostCheckMiddleware(session_pool=AsyncSessionLocal))

@router.message(Command("setup_schedule"))
async def setup_chedule(message: Message):
    await message.answer("Налаштувати графік", reply_markup=setup_schedule_keyboard())