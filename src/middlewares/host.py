from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.context import FSMContext
from aiogram.dispatcher.flags import get_flag
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.database.crud.users import get_role
from src.database.models import UserRole
from src.states.user_states import SignUp

class HostCheckMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
            self, 
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
            event: TelegramObject, 
            data: Dict[str, Any]
    ) -> Any:
        
        state: FSMContext = data.get("state")
        user = data.get("event_from_user")

        if not user:
            await event.answer("Щоб налаштувати розклад треба зареєструватись та змінити статус акаунту командою /become_host")
            await state.set_state(SignUp.start_reg)
            return


        user_id = user.id
        
        async with self.session_pool() as session:
            role = await get_role(session, user_id)

            if role != UserRole.HOST:
                await event.answer("Щоб налаштувати розклад треба змінити статус акаунту. Використайте команду /become_host")
                return
            
        return await handler(event, data)
        