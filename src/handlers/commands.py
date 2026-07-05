from aiogram import Router
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Бот запущено")

@router.message(Command("book_time"))
async def open_schedule(message: Message):
    button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Відкрити застосунок",
            web_app=WebAppInfo(url="https://uncrystallized-daisey-uninterwoven.ngrok-free.dev/")
        )]
    ])

    await message.answer("Забронювати час", reply_markup=button)

@router.message(Command("admin"))
async def open_admin(message: Message):
    button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Відкрити застосунок",
            web_app=WebAppInfo(url="https://uncrystallized-daisey-uninterwoven.ngrok-free.dev/admin/dashboard/index.html")
        )]
    ])

    await message.answer("Відкрити адмінську панель", reply_markup=button)