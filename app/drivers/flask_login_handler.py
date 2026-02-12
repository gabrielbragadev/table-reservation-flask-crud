from flask_login import (
    current_user,
    login_user as flask_login_user,
    logout_user as flask_logout_user,
)
from app.domain.entities.user import User


class FlaskLoginHandler:

    def login(self, user: User) -> None:
        flask_login_user(user)

    def logout(self) -> None:
        flask_logout_user()

    def is_authenticated(self) -> bool:
        is_user_authenticated = current_user.is_authenticated
        return is_user_authenticated

    def find_current_user_id(self) -> int:
        if not self.is_authenticated():
            return None
        return current_user.id

    def find_current_user_is_authenticated(self) -> bool:
        return current_user.is_authenticated
