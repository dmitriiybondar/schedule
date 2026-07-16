from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.dispatcher.flags import get_flag
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.ext.asyncio import async_sessionmaker

class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: Dict[str, Any]
    ) -> Any:

        use_db = get_flag(data, "use_db")

        if not use_db:
            return await handler(event, data)

        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)