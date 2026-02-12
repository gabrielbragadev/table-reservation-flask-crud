from app.domain.entities.user import User
from app.domain.exceptions import ConflictError, NotFoundError
from app.domain.repositories.user_repository import UserRepository


class AuthRules:

    @staticmethod
    def has_active_session(request) -> None:
        if request.cookies.get("session"):
            raise ConflictError(message="Usuário já autenticado")

    @staticmethod
    def resolve_user_by_username(
        user_repository: UserRepository, username: str
    ) -> User:
        user = user_repository.find_by_username(username)
        if user is None:
            raise NotFoundError(message="Usuário não encontrado")
        return user
