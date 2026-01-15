from typing import Dict
from sqlalchemy.orm import Session
from app.drivers.bcrypt_handler import BcryptHandler

from app.domain.exceptions import ConflictError, ForbiddenError, UnauthorizedError
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.drivers.flask_login_handler import FlaskLoginHandler


class CreateUserService:

    def __init__(self, data: Dict, session: Session):
        self.__session = session
        self.__username = data.get("username")
        self.__password = str.encode(data.get("password"))
        self.__email = data.get("email")
        self.__role = data.get("role")
        self.__user_repository = UserRepository(self.__session)
        self.__bcrypt_handler = BcryptHandler()
        self.__hashed = self.__bcrypt_handler.generate_password_hash(self.__password)
        self.__flask_login_handler = FlaskLoginHandler()

    def to_execute(self) -> User:

        self.__validate_user_creation_without_auth()
        self.__validate_user_role_permission()
        self.__is_username_taken()

        user = User(
            username=self.__username,
            password=self.__hashed,
            email=self.__email,
            role=self.__role,
        )
        self.__user_repository.create(user)
        return user

    def __validate_user_creation_without_auth(self) -> None:
        registered_users = self.__user_repository.find_all()
        current_user_is_authenticated = (
            self.__flask_login_handler.find_current_user_is_authenticated()
        )

        if registered_users and not current_user_is_authenticated:
            raise UnauthorizedError(
                message="Sessão inválida ou expirada. Faça login novamente."
            )

    def __validate_user_role_permission(self) -> None:

        current_user_is_authenticated = (
            self.__flask_login_handler.find_current_user_is_authenticated()
        )

        if not current_user_is_authenticated:
            return

        current_user_id = self.__flask_login_handler.find_current_user_id()
        authenticated_user = self.__user_repository.find_by_id(current_user_id)

        if authenticated_user.role == "user":
            raise ForbiddenError(
                message="Você não tem permissão para realizar esta ação."
            )

    def __is_username_taken(self) -> None:
        users_with_same_username = self.__user_repository.find_by_username(
            self.__username
        )
        if users_with_same_username:
            raise ConflictError(
                message="Já existe usuário cadastrado com esse username"
            )
