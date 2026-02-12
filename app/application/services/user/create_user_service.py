from app.domain.rules.user_rules import UserRules
from app.domain.uow.unit_of_work import UnitOfWork
from app.drivers.interfaces.flask_login_handler_interface import (
    FlaskLoginHandlerInterface,
)

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository

from app.application.commands.user.create_user_command import CreateUserCommand


class CreateUserService:

    def __init__(
        self,
        user_repository: UserRepository,
        flask_login_handler: FlaskLoginHandlerInterface,
        unit_of_work: UnitOfWork,
    ):
        self.__user_repository = user_repository
        self.__flask_login_handler = flask_login_handler
        self.__command = None
        self.__uow = unit_of_work

    def to_execute(self, command: CreateUserCommand) -> User:

        self.__command = command

        self.__require_auth_to_create_user_if_users_exist()
        self.__ensure_user_role_can_create_user()
        self.__ensure_username_is_available()
        self.__ensure_email_is_available()

        user = User(
            username=self.__command.data.username,
            email=self.__command.data.email,
            password=self.__command.data.password,
            role=self.__command.data.role,
        )

        self.__user_repository.save(user)
        self.__uow.commit()

        return user

    def __require_auth_to_create_user_if_users_exist(self) -> None:
        UserRules.validate_user_creation_without_auth(
            self.__user_repository, self.__flask_login_handler
        )

    def __ensure_user_role_can_create_user(self) -> None:
        UserRules.validate_user_role_permission(self.__command)

    def __ensure_username_is_available(self) -> None:
        UserRules.validate_username_conflict(
            self.__user_repository, self.__command.data.username
        )

    def __ensure_email_is_available(self) -> None:
        UserRules.validate_email_conflict(
            self.__user_repository, self.__command.data.email
        )
