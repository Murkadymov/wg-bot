from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(F.text.in_(["/instruction", "инструкция", "Инструкция"]))
async def instruction(message: types.Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Получить VPN", callback_data="getvpn")]
        ]
    )

    await message.answer(
        """📖 Инструкция по подключению VPN:

1️⃣ Установите приложение WireGuard:
   • Android/iOS: App Store / Google Play
   • Windows/macOS/Linux: https://www.wireguard.com/install/

2️⃣ Скачайте свой персональный конфиг в этом боте.

3️⃣ Импортируйте его в WireGuard:
   • Нажмите ➕ (Add tunnel)  
   • Выберите «Импорт из файла»  
   • Укажите скачанный конфиг.  

4️⃣ Включите VPN одним нажатием — готово 🎉

💡 Конфиг персональный, никому не передавайте.
""",
        reply_markup=kb
    )

