from app.application.commands.user.read_users_command import ReadUsersCommand
from app.application.dtos.user.read_user_dto import ReadUserDTO
from app.application.dtos.user.read_users_dto import ReadUsersDTO

from app.domain.exceptions import NotFoundError
from app.domain.repositories.user_repository import UserRepository
from app.domain.rules.user_rules import UserRules


class GetUsersServices:
    def __init__(self, user_repository: UserRepository) -> ReadUsersDTO:
        self.__user_repository = user_repository
        self.__users = None

    def to_execute(self, command: ReadUsersCommand):
        self.__get_all_users()

        UserRules.validate_user_role_permission(command)

        dtos = [ReadUserDTO(u.username, u.email, u.role) for u in self.__users]

        return ReadUsersDTO(users=dtos)

    def __get_all_users(self) -> None:
        self.__users = self.__user_repository.find_all()

        if self.__users is None:
            raise NotFoundError(message="Nenhum registro encontrado")
