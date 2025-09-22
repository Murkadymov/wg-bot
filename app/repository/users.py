from typing import Optional
from sqlalchemy import text
from app.db import engine


class UserRepository:
    @staticmethod
    def add_user(user_id: int, username: Optional[str], full_name: Optional[str], public_key: str, ip_address: str) -> None:
        """Сохраняем нового пользователя"""
        query = text("""
            INSERT INTO vpn_users (user_id, username, full_name, public_key, ip_address)
            VALUES (:user_id, :username, :full_name, :public_key, :ip_address)
            ON CONFLICT (user_id) DO NOTHING;
        """)
        with engine.begin() as conn:
            conn.execute(query, {
                "user_id": user_id,
                "username": username,
                "full_name": full_name,
                "public_key": public_key,
                "ip_address": ip_address,
            })

    @staticmethod
    def get_user(user_id: int) -> Optional[dict]:
        """Возвращаем пользователя по user_id"""
        query = text("SELECT * FROM vpn_users WHERE user_id = :user_id")
        with engine.begin() as conn:
            result = conn.execute(query, {"user_id": user_id}).mappings().first()
            return dict(result) if result else None

    @staticmethod
    def exists(user_id: int) -> bool:
        """Проверяем, есть ли пользователь"""
        query = text("SELECT 1 FROM vpn_users WHERE user_id = :user_id")
        with engine.begin() as conn:
            result = conn.execute(query, {"user_id": user_id}).first()
            return result is not None
