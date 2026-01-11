from typing import Dict
from sqlalchemy.orm import Session
from app.drivers.bcrypt_handler import BcryptHandler

from app.exceptions import ConflictError, ForbiddenError, UnauthorizedError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.drivers.flask_login_handler import FlaskLoginHandler


class CreateUserService:

    def __init__(self, data: Dict, session: Session):
        self.username = data.get("username")
        self.password = str.encode(data.get("password"))
        self.email = data.get("email")
        self.role = data.get("role")
        self.user_repository = UserRepository(session)
        self.bcrypt_handler = BcryptHandler()
        self.hashed = self.bcrypt_handler.generate_password_hash(self.password)
        self.flask_login_handler = FlaskLoginHandler()

    def create_user(self) -> User:

        self.__validate_user_creation_without_auth()
        self.__validate_user_role_permission()
        self.__is_username_taken()

        user = User(
            username=self.username,
            password=self.hashed,
            email=self.email,
            role=self.role,
        )
        self.user_repository.create(user)
        return user

    def __validate_user_creation_without_auth(self) -> None:
        registered_users = self.user_repository.find_all()
        current_user_is_authenticated = (
            self.flask_login_handler.find_current_user_is_authenticated()
        )

        if registered_users and not current_user_is_authenticated:
            raise UnauthorizedError(
                message="Sessão inválida ou expirada. Faça login novamente."
            )

    def __validate_user_role_permission(self) -> None:

        current_user_is_authenticated = (
            self.flask_login_handler.find_current_user_is_authenticated()
        )

        if not current_user_is_authenticated:
            return

        current_user_id = self.flask_login_handler.find_current_user_id()
        authenticated_user = self.user_repository.find_by_id(current_user_id)

        if authenticated_user.role == "user":
            raise ForbiddenError(
                message="Você não tem permissão para realizar esta ação."
            )

    def __is_username_taken(self) -> None:
        users_with_same_username = self.user_repository.find_by_username(self.username)
        if users_with_same_username:
            raise ConflictError(
                message="Já existe usuário cadastrado com esse username"
            )
