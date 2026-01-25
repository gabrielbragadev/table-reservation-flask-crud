from app.application.commands.user.update_user_command import UpdateUserCommand
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.rules.user_rules import UserRules
from app.drivers.interfaces.bcrypt_handler_interface import BcryptHandlerInterface
from app.infrastructure.persistence.sqlalchemy.unit_of_work import UnitOfWork


class UpdateUserService:
    def __init__(
        self,
        user_repository: UserRepository,
        bcrypt_handler: BcryptHandlerInterface,
        unit_of_work: UnitOfWork,
    ):
        self.__user_repository = user_repository
        self.__bcrypt_handler = bcrypt_handler
        self.__command = None
        self.__user_to_be_changed = None
        self.__hash_password = None
        self.__uow = unit_of_work

    def to_execute(self, command: UpdateUserCommand) -> User:

        self.__command = command

        self.__generate_password_hash()
        self.__get_user_to_be_changed()

        self.__ensure_user_cannot_edit_others()
        self.__is_username_taken()
        self.__is_email_taken()

        self.__ensure_role_edit_permission()
        self.__user_to_be_changed.role = self.__command.dto.role

        if self.__command.dto.username:
            self.__user_to_be_changed.username = self.__command.dto.username

        if self.__command.dto.password:
            self.__user_to_be_changed.password = self.__hash_password

        if self.__command.dto.email:
            self.__user_to_be_changed.email = self.__command.dto.email

        self.__uow.commit()

        return self.__user_to_be_changed

    def __get_user_to_be_changed(self) -> None:
        self.__user_to_be_changed = UserRules.get_user_to_be_changed(
            self.__user_repository, self.__command
        )

    def __generate_password_hash(self) -> None:
        self.__hash_password = self.__bcrypt_handler.generate_hash(
            self.__command.dto.password
        )

    def __is_username_taken(self) -> None:
        UserRules.validate_username_conflict(
            self.__user_repository, self.__command.dto.username
        )

    def __is_email_taken(self) -> None:
        UserRules.validate_email_conflict(
            self.__user_repository, self.__command.dto.email
        )

    def __ensure_user_cannot_edit_others(self) -> None:
        UserRules.validate_user_cannot_update_others(
            self.__user_to_be_changed, self.__command
        )

    def __ensure_role_edit_permission(self):
        if self.__command.dto.role:
            UserRules.validate_user_role_permission(self.__command)
