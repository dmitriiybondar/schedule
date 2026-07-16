from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.users import create_user, change_params
from database.connection import AsyncSessionLocal

from middlewares.database import DbSessionMiddleware
from states.user_states import SignUp, ChangeParams
from keyboards import get_schedule_keyboard

router = Router()
router.message.middleware(DbSessionMiddleware(session_pool=AsyncSessionLocal))

async def sign_up(message: Message, state: FSMContext, next_action: str = None):
    user_id = message.from_user.id
    username = message.from_user.username

    await state.update_data(
        telegram_id=user_id,
        username=username,
        next_action=next_action
    )

    await state.set_state(SignUp.full_name)
    await message.answer("Введіть своє ПІБ")


@router.message(SignUp.full_name)
async def full_name(message: Message, state: FSMContext):
    name = message.text

    button = KeyboardButton(text="Поділитись номером", request_contact=True)
    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await state.update_data(full_name=name)
    await state.set_state(SignUp.phone_number)
    await message.answer("Надайте всій номер телефону", reply_markup=contact_keyboard)


@router.message(SignUp.phone_number, F.contact, flags={"use_db": True})
async def contact_success(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()

    phone = message.contact.phone_number
    telegram_id = int(data["telegram_id"])
    username = data["username"]
    full_name = data["full_name"]
    next_action = data["next_action"]

    await create_user(session, telegram_id, username, full_name, phone)
    await message.answer("Реєстрація успішно завершена")

    if next_action == "open_schedule":
        await message.answer("Забронювати час", reply_markup=get_schedule_keyboard())

    await state.clear()
    

@router.message(SignUp.phone_number)
async def contact_fail(message: Message):
    await message.answer("Для реєстрації необхідно натиснути кнопку \"Поділитись номером\". Не намагайтесь вводити текст вручну")



@router.message(Command("change_name"))
async def change_name(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(
        telegram_id=user_id,
        column = "full_name"    
    )
    await state.set_state(ChangeParams.value)
    await message.answer("Введіть нове ім'я")

# @router.message(Command("change_role"))
# async def change_name(message: Message, state: FSMContext):
#     user_id = message.from_user.id

#     await state.update_data(
#         telegram_id=user_id,
#         column = "role"    
#     )
#     await state.set_state(ChangeParams.value)
#     await message.answer("Введіть нову роль")

@router.message(ChangeParams.value, flags={"use_db": True})
async def new_data(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()

    value = message.text
    column = data["column"]
    telegram_id = data["telegram_id"]

    await change_params(session, telegram_id, column, value)

    await message.answer("Значення успішно змінено")
    await state.clear()
