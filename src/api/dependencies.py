from fastapi import Header, HTTPException
from aiogram import Bot
from aiogram.utils.web_app import safe_parse_webapp_init_data

from src.bot import BOT_TOKEN

async def get_telegram_id(x_telegram_init_data: str = Header()):
    try:
        web_app_data = safe_parse_webapp_init_data(
            token=BOT_TOKEN,
            init_data=x_telegram_init_data
        )

        return web_app_data.user.id

    except ValueError:
        raise HTTPException(status_code=403, detail="Недійсні дані авторизації Telegram")
