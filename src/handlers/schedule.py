from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.connection import AsyncSessionLocal
from database.crud.users import get_user
from keyboards import get_schedule_keyboard
from .user import sign_up

router = Router()

@router.message(Command("book_time"))
async def open_schedule(message: Message, state: FSMContext):
    user_id = message.from_user.id

    async with AsyncSessionLocal() as session:
        user = await get_user(session, user_id)

    if user:
        await message.answer("Забронювати час", reply_markup=get_schedule_keyboard())

    else:
        await message.answer("Для початку пройдіть реєстрацію. Вона проходиться один раз при першому бронюванні")
        await sign_up(message, state, next_action = "open_schedule")