from app.domain.rules.auth_rules import AuthRules
from app.drivers.interfaces.bcrypt_handler_interface import BcryptHandlerInterface
from app.drivers.interfaces.flask_login_handler_interface import (
    FlaskLoginHandlerInterface,
)

from app.domain.exceptions import UnauthorizedError
from app.domain.repositories.user_repository import UserRepository
from app.domain.rules.auth_rules import AuthRules
from app.application.commands.auth.user_login_command import UserLoginCommand


class UserLoginService:
    def __init__(
        self,
        bcrypt_handler: BcryptHandlerInterface,
        user_repository: UserRepository,
        flask_login_handler: FlaskLoginHandlerInterface,
    ):
        self.__bcrypt_handler = bcrypt_handler
        self.__flask_login_handler = flask_login_handler
        self.__user = None
        self.__command = None
        self.__user_repository = user_repository

    def user_login(self, command: UserLoginCommand, request) -> None:
        self.__command = command

        self.__has_active_session(request)
        self.__get_user_by_username()
        self.__is_password_correct()

        self.__flask_login_handler.login(self.__user)
        return self.__user

    def __has_active_session(self, request):
        AuthRules.has_active_session(request)

    def __get_user_by_username(self) -> None:
        self.__user = AuthRules.resolve_user_by_username(
            self.__user_repository, self.__command.dto.username
        )

    def __is_password_correct(self):
        if not self.__bcrypt_handler.verify_hash(
            self.__user, self.__command.dto.password
        ):
            raise UnauthorizedError(message="Credenciais Inválidas")
