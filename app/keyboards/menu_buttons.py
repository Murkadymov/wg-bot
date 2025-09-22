from aiogram import types


def menu_buttons() -> types.ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text="Инструкция"), types.KeyboardButton(text="Получить VPN")],
        [types.KeyboardButton(text="Помощь")],

    ]
    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите раздел",
        one_time_keyboard=True,
    )
