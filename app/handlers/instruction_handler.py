from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.filters.instruction_filter import InstructionFilter
from app.handlers.get_vpn import get_vpn

router = Router()

@router.message(InstructionFilter())
async def instruction(message: types.Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Получить VPN", callback_data="getvpn")]
        ]
    )

    await message.answer(
        """📖 Инструкция по подключению VPN:

1️⃣ Установи приложение WireGuard:
   • Android/iOS: App Store / Google Play
   • Windows/macOS/Linux: https://www.wireguard.com/install/

2️⃣ Скачай свой персональный конфиг в этом боте.

3️⃣ Импортируй его в WireGuard:
   • Нажми ➕ (Add tunnel)  
   • Выбери «Импорт из файла»  
   • Укажи скачанный конфиг.  

4️⃣ Включи VPN одним нажатием — готово 🎉

💡 Конфиг персональный, никому не передавай.
""",
        reply_markup=kb
    )

@router.callback_query(F.data == "getvpn")
async def handle_getvpn_callback(callback: types.CallbackQuery):
    await get_vpn(callback.message)
    await callback.answer()
