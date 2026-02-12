from typing import Any, Dict
from app.application.commands.user.read_user_command import ReadUserCommand
from app.domain.exceptions import NotFoundError
from app.domain.repositories.user_repository import UserRepository
from app.domain.rules.user_rules import UserRules


class GetUserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.__user_repository = user_repository
        self.__user_to_read = None
        self.__command = None

    def to_execute(self, command: ReadUserCommand) -> Dict[str, Any]:
        self.__command = command

        UserRules.validate_user_cannot_view_others(self.__command)

        self.__get_user_to_read()
        self.__validate_user_exists()

        return_dict = self.__to_fill_return_dict()

        return return_dict

    def __get_user_to_read(self) -> None:
        self.__user_to_read = self.__user_repository.find_by_id(self.__command.user_id)

    def __is_user_nonexistent(self) -> bool:
        return self.__user_to_read is None

    def __not_found_exception(self) -> None:
        raise NotFoundError(message="Usuário não encontrado")

    def __validate_user_exists(self):
        if self.__is_user_nonexistent():
            self.__not_found_exception()

    def __to_fill_return_dict(self) -> Dict[str, Any]:
        return {
            "username": self.__user_to_read.username,
            "email": self.__user_to_read.email,
            "role": self.__user_to_read.role,
        }
