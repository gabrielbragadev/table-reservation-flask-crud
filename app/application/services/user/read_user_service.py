from app.application.commands.user.read_user_command import ReadUserCommand
from app.domain.entities.user import User
from app.domain.exceptions import NotFoundError
from app.domain.repositories.user_repository import UserRepository
from app.domain.rules.user_rules import UserRules


class GetUserService:
    def __init__(self, user_repository: UserRepository) -> User:
        self.__user_repository = user_repository

    def to_execute(self, command: ReadUserCommand) -> User:

        UserRules.validate_user_cannot_view_others(command)

        user = self.__user_repository.find_by_id(command.user_id)
        if not user:
            raise NotFoundError(message="Usuário não encontrado")

        return user
