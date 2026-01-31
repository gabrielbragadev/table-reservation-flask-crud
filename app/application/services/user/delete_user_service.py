from typing import Dict

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.uow.unit_of_work import UnitOfWork
from app.drivers.interfaces.cryptocode_handler_interface import (
    CryptocodeHandlerInterface,
)
from app.drivers.interfaces.flask_login_handler_interface import (
    FlaskLoginHandlerInterface,
)
from app.application.commands.user.delete_user_command import DeleteUserCommand
from app.domain.rules.user_rules import UserRules


class DeleteUserService:
    def __init__(
        self,
        user_repository: UserRepository,
        flask_login_handler: FlaskLoginHandlerInterface,
        unit_of_work: UnitOfWork,
        cryptocode_handler: CryptocodeHandlerInterface,
    ) -> None:
        self.__user_repository = user_repository
        self.__flask_login_handler = flask_login_handler
        self.__command = None
        self.__user_to_delete = None
        self.__uow = unit_of_work
        self.__cryptocode_handler = cryptocode_handler

    def to_execute(self, command: DeleteUserCommand) -> Dict[User]:
        self.__command = command
        self.get_user_to_delete()

        UserRules.validate_user_cannot_view_others(self.__command)
        self.get_user_to_delete()

        self.__validate_self_delete_otp()

        self.__user_repository.delete(self.__user_to_delete)
        self.__uow.commit()

        if self.__is_self_delete():
            self.__flask_login_handler.logout()

        return self.__user_to_delete

    def get_user_to_delete(self) -> None:
        self.__user_to_delete = UserRules.get_and_validate_user_to_delete(
            self.__user_repository, self.__command.user_id
        )

    def __is_self_delete(self) -> bool:
        return self.__command.user_id == self.__command.requester_user_id

    def __validate_self_delete_otp(self):
        if self.__is_self_delete():
            UserRules.validate_self_delete_otp(
                self.__user_to_delete,
                self.__command.otp_code,
                self.__cryptocode_handler,
            )
