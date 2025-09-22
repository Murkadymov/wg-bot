from aiogram import Router, F, types

from app.keyboards.menu_buttons import menu_buttons

router = Router()

MENU_TRIGGERS = {"меню", "/menu"}

@router.message(F.text.func(lambda t: (t or "").strip().lower() in MENU_TRIGGERS) # ещё поправил фильтр
async def menu(message: types.Message):
    kb = menu_buttons()

    await message.answer(
        "В Меню выберите подходящий раздел",
        reply_markup=kb
    )