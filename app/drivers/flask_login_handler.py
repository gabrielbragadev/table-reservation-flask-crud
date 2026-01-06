from flask_login import (
    current_user,
    login_user as flask_login_user,
    logout_user as flask_logout_user,
)
from app.models.user import User


class FlaskLoginHandler:

    @staticmethod
    def login(user: User) -> None:
        flask_login_user(user)

    @staticmethod
    def logout() -> None:
        flask_logout_user()

    @staticmethod
    def is_authenticated() -> bool:
        is_user_authenticated = current_user.is_authenticated
        return is_user_authenticated

    @staticmethod
    def get_user_id() -> int:
        return current_user.id
