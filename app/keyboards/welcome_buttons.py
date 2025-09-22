from aiogram import types


def welcome_menu_keyboard() -> types.ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text="Меню"), types.KeyboardButton(text="Выйти из меню")],
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбери раздел",
        one_time_keyboard=True,
        one_time_message_keyboard=True,
    )