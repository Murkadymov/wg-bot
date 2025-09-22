import subprocess
from aiogram import Router, types, F
from aiogram.types import FSInputFile
from sqlalchemy.exc import DatabaseError

from app.keyboards.menu_buttons import menu_buttons
from app.logger.setup_logger import get_logger
from app.models.user import UserModel
from app.repository.users import UserRepository
from app.vpnmanager.generate_client import generate_client_conf, add_peer_persistent
from app.vpnmanager.keys import generate_private_key, generate_public_key
from app.vpnmanager.parser import get_next_free_ip

logger = get_logger(__name__)
router = Router()


async def _issue_vpn_for(user: types.User, reply_to: types.Message):
    """Общая логика: выдать VPN-конфиг для пользователя."""
    kb = menu_buttons()

    db_user = UserModel(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
    )

    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    free_ip = get_next_free_ip()

    # генерируем client.conf
    try:
        conf_path = generate_client_conf(db_user.id, private_key, free_ip)
    except OSError:
        logger.exception(f"Ошибка доступа к файлу при генерации client.conf для user_id={db_user.id}")
        await reply_to.answer("Не удалось создать VPN конфиг (ошибка файловой системы) 🙏")
        return
    except Exception:
        logger.exception(f"Неизвестная ошибка при генерации client.conf для user_id={db_user.id}")
        await reply_to.answer("Произошла ошибка при выдаче ВПН, попробуйте позже 🙏")
        return

    # добавляем peer в wg0
    try:
        add_peer_persistent(public_key, free_ip)
    except subprocess.CalledProcessError:
        logger.exception(f"Команда wg завершилась с ошибкой для user_id={db_user.id}")
        await reply_to.answer("Ошибка при добавлении VPN-пользователя на сервер 🙏")
        return
    except Exception:
        logger.exception(f"Неизвестная ошибка при добавлении peer для user_id={db_user.id}")
        await reply_to.answer("Произошла ошибка при настройке VPN, попробуйте позже 🙏")
        return

    conf_file = FSInputFile(conf_path)

    try:
        UserRepository.add_user(
            user_id=db_user.id,
            username=db_user.username,
            full_name=db_user.full_name,
            public_key=public_key,
            ip_address=free_ip,
        )
    except Exception as e:
        logger.exception(f"Ошибка при добавлении пользователя {db_user.id} в базу")
        raise DatabaseError("Не удалось сохранить пользователя в БД") from e

    await reply_to.answer_document(
        document=conf_file,
        caption="Вот твой VPN-конфиг 🚀\nИмпортируй его в приложение WireGuard",
        reply_markup=kb,
    )


# --- Хендлеры ---

@router.message(F.text.in_(["/getvpn", "Получить VPN"]))
async def get_vpn_cmd(message: types.Message):
    await _issue_vpn_for(message.from_user, message)


@router.callback_query(F.data == "getvpn")
async def get_vpn_cb(callback: types.CallbackQuery):
    await _issue_vpn_for(callback.from_user, callback.message)
    await callback.answer()
