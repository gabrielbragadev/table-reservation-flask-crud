from app.drivers.interfaces.flask_login_handler_interface import (
    FlaskLoginHandlerInterface,
)
from app.domain.exceptions import ForbiddenError


class LogoutService:
    def __init__(self, flask_login_handler: FlaskLoginHandlerInterface):
        self.__flask_login_handler = flask_login_handler

    def user_logout_service(self) -> None:

        self.__is_authenticated()
        self.__flask_login_handler.logout()

    def __is_authenticated(self):
        if self.__flask_login_handler.find_current_user_is_authenticated():
            return
        raise ForbiddenError(
            message="É necessário estar autenticado para realizar logout"
        )
