from aiogram import Router, F, types

from app.keyboards.menu_buttons import menu_buttons

router = Router()

@router.message(F.text == "Меню")   # ещё поправил фильтр
async def menu(message: types.Message):
    kb = menu_buttons()

    await message.answer(
        "Нажмите на кнопку раздела 'Инструкция' для получения следующих шагов",
        reply_markup=kb
    )