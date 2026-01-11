from app.drivers.flask_login_handler import FlaskLoginHandler
from app.exceptions import ForbiddenError


def user_logout_service() -> None:
    flask_login_handler = FlaskLoginHandler()

    if flask_login_handler.get_current_user_id().is_authenticated:
        flask_login_handler.logout()
    raise ForbiddenError(message="É necessário estar autenticado para realizar logout")
