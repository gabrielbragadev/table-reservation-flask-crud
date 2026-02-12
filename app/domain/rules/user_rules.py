import pyotp
from app.application.commands.user.create_user_command import CreateUserCommand
from app.application.commands.user.delete_user_command import DeleteUserCommand
from app.application.commands.user.update_user_command import UpdateUserCommand
from app.application.commands.user.user_ownership_command import UserOwnershipCommand
from app.domain.entities.user import User
from app.domain.exceptions import (
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)
from app.domain.repositories.user_repository import UserRepository
from app.drivers.interfaces.flask_login_handler_interface import (
    FlaskLoginHandlerInterface,
)
from app.drivers.interfaces.cryptocode_handler_interface import (
    CryptocodeHandlerInterface,
)


class UserRules:

    @staticmethod
    def validate_user_creation_without_auth(
        user_repository: UserRepository,
        flask_login_handler: FlaskLoginHandlerInterface,
    ) -> None:

        registered_users = user_repository.find_all()
        current_user_is_authenticated = (
            flask_login_handler.find_current_user_is_authenticated()
        )
        if registered_users and not current_user_is_authenticated:
            raise UnauthorizedError(
                message="Sessão inválida ou expirada. Faça login novamente."
            )

    @staticmethod
    def validate_user_role_permission(command: UserOwnershipCommand) -> None:

        if command.requester_role and command.requester_role != "admin":
            raise ForbiddenError(message="Ação permitida apenas para administradores.")

    @staticmethod
    def validate_user_cannot_view_others(command: UserOwnershipCommand) -> None:
        if command.user_id != command.requester_user_id:
            UserRules.validate_user_role_permission(command)

    @staticmethod
    def validate_user_cannot_update_others(
        user: User, command: UpdateUserCommand
    ) -> None:
        if user.id != command.requester_user_id:
            UserRules.validate_user_role_permission(command)

    @staticmethod
    def validate_username_conflict(user_repository: UserRepository, username: str):
        users_with_same_username = user_repository.find_by_username(username)
        if users_with_same_username:
            raise ConflictError(
                message="Já existe usuário cadastrado com esse username"
            )

    @staticmethod
    def validate_email_conflict(user_repository: UserRepository, email: str):
        users_with_same_email = user_repository.find_by_email(email)
        if users_with_same_email:
            raise ConflictError(message="Já existe usuário cadastrado com esse email")

    @staticmethod
    def get_and_validate_user_to_delete(
        user_repository: UserRepository, user_id: int
    ) -> User:
        user = user_repository.find_by_id(user_id)

        if user is None:
            raise NotFoundError(message="Registro não encontrado")
        return user

    @staticmethod
    def get_user_to_be_changed(
        user_repository: UserRepository, command: UpdateUserCommand
    ) -> User:
        user = user_repository.find_by_id(command.user_id)

        if user is None:
            user = user_repository.find_by_id(command.requester_user_id)

        return user

    @staticmethod
    def validate_self_delete_otp(
        user: User, otp_code: str | None, cryptocode_handler: CryptocodeHandlerInterface
    ):
        if not otp_code:
            raise UnauthorizedError(message="Código 2FA é obrigatório")

        two_fa_secret = cryptocode_handler.decrypting(user.two_fa_secret)
        totp = pyotp.TOTP(two_fa_secret)

        if not totp.verify(otp_code, valid_window=1):
            raise UnauthorizedError(message="Código 2FA inválido ou expirado")
