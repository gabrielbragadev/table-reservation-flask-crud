from app.domain.entities.user import User
from app.domain.exceptions import NotFoundError
from app.domain.repositories.user_repository import UserRepository


class AuthRules:

    def resolve_user_by_username(
        user_repository: UserRepository, username: str
    ) -> User:
        user = user_repository.find_by_username(username)
        if user is None:
            raise NotFoundError(message="Usuário não encontrado")
        return user
