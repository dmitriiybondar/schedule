from aiogram.fsm.state import State, StatesGroup

class SignUp(StatesGroup):
    full_name = State()
    phone_number = State()