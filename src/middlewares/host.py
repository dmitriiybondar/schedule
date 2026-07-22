from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.context import FSMContext
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.database.crud.users import get_role, get_user
from src.database.models import UserRole
from src.states.user_states import SignUp
from src.enums import RegActions

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
        tg_user = data.get("event_from_user")

        if not tg_user:
            return
        
        user_id = tg_user.id
        
        async with self.session_pool() as session:
            user = await get_user(session, user_id)

            if not user:
                await state.update_data(
                    telegram_id=user_id,
                    username=tg_user.username,
                    next_action=RegActions.SETUP_SCHEDULE
                )
                await event.answer("Для початку необхідно зареєструватись")
                await event.answer("Введіть своє ПІБ")
                await state.set_state(SignUp.full_name)

                return
            
            role = await get_role(session, user_id)

            if role != UserRole.HOST:
                await event.answer("Щоб налаштувати розклад треба змінити статус акаунту. Використайте команду /become_host")
                return
            
        return await handler(event, data)
        