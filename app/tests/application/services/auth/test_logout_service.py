# pytest .\app\tests\application\services\auth\test_logout_service.py -s -v

import pytest
from unittest.mock import Mock

from app.application.services.auth.logout_service import LogoutService
from app.domain.exceptions import ForbiddenError


@pytest.fixture
def flask_login_handler():
    handler = Mock()
    handler.find_current_user_is_authenticated.return_value = True
    return handler


@pytest.fixture
def service(flask_login_handler):
    return LogoutService(flask_login_handler=flask_login_handler)


def test_logout_not_authenticated_raises_forbidden_error(
    service,
    flask_login_handler,
):
    flask_login_handler.find_current_user_is_authenticated.return_value = False

    with pytest.raises(ForbiddenError) as exc:
        service.user_logout_service()

    assert "É necessário estar autenticado" in str(exc.value)


def test_logout_not_called_when_user_not_authenticated(
    service,
    flask_login_handler,
):
    flask_login_handler.find_current_user_is_authenticated.return_value = False

    with pytest.raises(ForbiddenError):
        service.user_logout_service()

    flask_login_handler.logout.assert_not_called()


def test_authentication_check_is_called(service, flask_login_handler):
    service.user_logout_service()

    flask_login_handler.find_current_user_is_authenticated.assert_called_once()
