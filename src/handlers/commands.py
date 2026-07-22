from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Бот запущено")
    

@router.message(Command("cancel"))
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Дія скасована")