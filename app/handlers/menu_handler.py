from aiogram import Router, F, types

from app.keyboards.menu_buttons import menu_buttons

router = Router()

@router.message(F.text.in_(["menu", "Меню", "/menu"])) # ещё поправил фильтр
async def menu(message: types.Message):
    kb = menu_buttons()

    await message.answer(
        "В Меню выберите подходящий раздел",
        reply_markup=kb
    )