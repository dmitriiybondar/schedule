from aiogram import Router
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Бот запущено")

@router.message(Command("site"))
async def site(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Відкрити сайт",
            web_app=WebAppInfo(url="https://uncrystallized-daisey-uninterwoven.ngrok-free.dev/")
        )]
    ])

    await message.answer("Натисни кноопку", reply_markup=keyboard)