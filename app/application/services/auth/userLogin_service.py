from typing import Dict
from app.drivers.bcrypt_handler import BcryptHandler
from app.drivers.flask_login_handler import FlaskLoginHandler

from app.domains.exceptions import UnauthorizedError
from app.domains.repositories.user_repository import UserRepository


def user_login_service(data: Dict) -> None:
    bcrypt_handler = BcryptHandler()
    flask_login_handler = FlaskLoginHandler()
    user_repository = UserRepository()

    username = data.get("username")
    password = str.encode(data.get("password"))
    user = user_repository.find_by_username(username)

    if user and bcrypt_handler.verify_password(user, password):
        flask_login_handler.login(user)

    raise UnauthorizedError(message="Credenciais Inválidas")
