from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_schedule_keyboard():
    link = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Відкрити застосунок",
            web_app=WebAppInfo(url="https://uncrystallized-daisey-uninterwoven.ngrok-free.dev/")
        )]
    ])
    
    return link