from aiogram import Router
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Бот запущено")
    