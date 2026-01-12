from typing import Dict
from sqlalchemy.orm import Session

from app.exceptions import ForbiddenError, NotFoundError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.drivers.flask_login_handler import FlaskLoginHandler


class DeleteUserService:
    def __init__(self, user_id: int, session: Session) -> None:
        self.__session = session
        self.__user_repository = UserRepository(self.__session)
        self.__flask_login_handler = FlaskLoginHandler()
        self.__user_id = user_id

    def to_execute(self) -> Dict[User]:
        self.__user = self.__user_repository.find_by_id(self.__user_id)
        self.__current_user_id = self.__flask_login_handler.find_current_user_id()

        self.__validate_not_modifying_self()
        self.__validate_user_cannot_delete_others()
        self.__check_user_exists()

        self.__user_repository.delete(self.__user)
        return self.__user.to_dict()

    def __validate_not_modifying_self(self) -> None:
        if self.__current_user_id == self.__user_id:
            raise ForbiddenError(
                message="Você não pode excluir seu próprio usuário enquanto estiver logado"
            )

    def __validate_user_cannot_delete_others(self) -> None:
        authenticated_user = self.__user_repository.find_by_id(self.__current_user_id)

        if authenticated_user.role == "user":
            raise ForbiddenError(
                message="Você não tem permissão pra realizar essa ação"
            )

    def __check_user_exists(self):
        if self.__user is None:
            raise NotFoundError("Registro não encontrado")
