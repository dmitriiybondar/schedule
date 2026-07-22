from enum import StrEnum
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import UserRole
from src.database.crud.users import create_user, change_params, get_role, get_user, delete_user
from src.database.connection import AsyncSessionLocal

from src.middlewares.database import DbSessionMiddleware
from src.states.user_states import SignUp, ChangeParams
from src.keyboards import get_schedule_keyboard, setup_schedule_keyboard
from src.enums import RegActions

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

    HOST_ACTIONS = {RegActions.BECOME_HOST, RegActions.SETUP_SCHEDULE}
    role = UserRole.HOST if next_action in HOST_ACTIONS else UserRole.USER

    await create_user(session, telegram_id, username, full_name, phone, role)
    rmw_keyboard = ReplyKeyboardRemove()


    if next_action == RegActions.OPEN_SCHEDULE:
        await message.answer("Реєстрація успішно завершена", reply_markup=rmw_keyboard)
        await message.answer("Забронювати час", reply_markup=get_schedule_keyboard())

    elif next_action == RegActions.BECOME_HOST:
        await message.answer("Акаунт успішно створено та надано роль адміна", reply_markup=rmw_keyboard)

    elif next_action == RegActions.SETUP_SCHEDULE:
        await message.answer("Акаунт успішно створено", reply_markup=ReplyKeyboardRemove())
        await message.answer("Налаштувати графік", reply_markup=setup_schedule_keyboard())
    
    else:
        await message.answer("Реєстрація завершена.", reply_markup=rmw_keyboard)

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


@router.message(ChangeParams.value, flags={"use_db": True})
async def new_data(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()

    value = message.text
    column = data["column"]
    telegram_id = data["telegram_id"]

    await change_params(session, telegram_id, column, value)

    await message.answer("Значення успішно змінено")
    await state.clear()


@router.message(Command("become_host"), flags={"use_db": True})
async def become_host(message: Message, session: AsyncSession, state: FSMContext):
    user_id = message.from_user.id
    cur_row = await get_role(session, user_id)
    user = await get_user(session, user_id)

    if not user:
        await message.answer("Спочатку вам необхідно пройти реєстрацію")
        await sign_up(message, state, next_action=RegActions.BECOME_HOST)
        return

    if cur_row == UserRole.USER:
        column = "role"
        value = UserRole.HOST

        await change_params(session, user_id, column, value)
        await message.answer("Роль успішно змінено")

    else:
        await message.answer("Ви вже і так адмін")


@router.message(Command("delete"), flags={"use_db": True})
async def delete_userr(message: Message, session: AsyncSession):
    user_id = message.from_user.id

    await delete_user(session, user_id)
    await message.answer("ok")

