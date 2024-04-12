from aiogram.fsm.state import StatesGroup, State


class FSMFillForm(StatesGroup):
    fill_text = State()  # Ожидание ввода текста от пользователя
