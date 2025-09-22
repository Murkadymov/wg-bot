import subprocess
from aiogram import Router, types
from aiogram.types import FSInputFile

from app.filters.get_vpn_filter import VPNRequestFilter
from app.keyboards.menu_buttons import menu_buttons
from app.logger.setup_logger import get_logger
from app.models.user import UserModel
from app.vpnmanager.generate_client import generate_client_conf, add_peer, add_peer_persistent
from app.vpnmanager.keys import generate_private_key, generate_public_key
from app.vpnmanager.parser import get_next_free_ip

logger = get_logger(__name__)
router = Router()


@router.message(VPNRequestFilter())
async def get_vpn(message: types.Message):
    kb = menu_buttons()

    user = UserModel(
        id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
    )

    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    free_ip = get_next_free_ip()

    # генерируем client.conf
    try:
        conf_path = generate_client_conf(user.id, private_key, free_ip)
    except OSError as e:
        logger.exception(f"Ошибка доступа к файлу при генерации client.conf для user_id={user.id}")
        await message.answer("Не удалось создать VPN конфиг (ошибка файловой системы) 🙏")
        return
    except Exception as e:
        logger.exception(f"Неизвестная ошибка при генерации client.conf для user_id={user.id}")
        await message.answer("Произошла ошибка при выдаче ВПН, попробуйте позже 🙏")
        return

    # добавляем peer в wg0
    try:
        add_peer_persistent(public_key, free_ip)
    except subprocess.CalledProcessError:
        logger.exception(f"Команда wg завершилась с ошибкой для user_id={user.id}")
        await message.answer("Ошибка при добавлении VPN-пользователя на сервер 🙏")
        return
    except Exception:
        logger.exception(f"Неизвестная ошибка при добавлении peer для user_id={user.id}")
        await message.answer("Произошла ошибка при настройке VPN, попробуйте позже 🙏")
        return

    # правильная передача файла
    conf_file = FSInputFile(conf_path)

    await message.answer_document(
        document=conf_file,
        caption="Вот твой VPN-конфиг 🚀\nИмпортируй его в приложение WireGuard",
        reply_markup=kb,
    )
