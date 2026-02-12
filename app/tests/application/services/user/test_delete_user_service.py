# run: pytest .\app\tests\application\services\user\test_delete_user_service.py -s -v
import pytest
from unittest.mock import Mock

from app.application.services.user.delete_user_service import DeleteUserService
from app.application.commands.user.delete_user_command import DeleteUserCommand
from app.domain.exceptions import ForbiddenError, NotFoundError
from app.domain.entities.user import User


# =========================
# FIXTURES BASE
# =========================

@pytest.fixture
def user():
    user = Mock(spec=User)
    user.id = 1
    return user


@pytest.fixture
def other_user():
    user = Mock(spec=User)
    user.id = 2
    return user


@pytest.fixture
def user_repository():
    return Mock()


@pytest.fixture
def flask_login_handler():
    handler = Mock()
    handler.logout = Mock()
    return handler


@pytest.fixture
def unit_of_work():
    uow = Mock()
    uow.commit = Mock()
    return uow


@pytest.fixture
def cryptocode_handler():
    return Mock()


@pytest.fixture
def service(
    user_repository,
    flask_login_handler,
    unit_of_work,
    cryptocode_handler,
):
    return DeleteUserService(
        user_repository=user_repository,
        flask_login_handler=flask_login_handler,
        unit_of_work=unit_of_work,
        cryptocode_handler=cryptocode_handler,
    )


# =========================
# TESTES
# =========================

def test_delete_other_user_success(
    service,
    mocker,
    user_repository,
    unit_of_work,
    other_user,
):
    mocker.patch(
        "app.domain.rules.user_rules.UserRules.get_and_validate_user_to_delete",
        return_value=other_user,
    )

    mocker.patch(
        "app.domain.rules.user_rules.UserRules.validate_user_cannot_view_others",
        return_value=None,
    )

    command = DeleteUserCommand(
        user_id=2,
        requester_user_id=1,
        requester_role="ADMIN",
        otp_code=None,
    )

    result = service.to_execute(command)

    user_repository.delete.assert_called_once_with(other_user)
    unit_of_work.commit.assert_called_once()
    assert result == other_user


def test_self_delete_with_valid_otp_success(
    service,
    mocker,
    user_repository,
    flask_login_handler,
    unit_of_work,
    user,
):
    mocker.patch(
        "app.domain.rules.user_rules.UserRules.get_and_validate_user_to_delete",
        return_value=user,
    )

    mocker.patch(
        "app.domain.rules.user_rules.UserRules.validate_user_cannot_view_others",
        return_value=None,
    )

    mocker.patch(
        "app.domain.rules.user_rules.UserRules.validate_self_delete_otp",
        return_value=None,
    )

    command = DeleteUserCommand(
        user_id=1,
        requester_user_id=1,
        requester_role="USER",
        otp_code="123456",
    )

    result = service.to_execute(command)

    user_repository.delete.assert_called_once_with(user)
    unit_of_work.commit.assert_called_once()
    flask_login_handler.logout.assert_called_once()
    assert result == user


def test_delete_other_user_forbidden(service, mocker):
    mocker.patch(
        "app.domain.rules.user_rules.UserRules.validate_user_cannot_view_others",
        side_effect=ForbiddenError("Operação não permitida"),
    )

    command = DeleteUserCommand(
        user_id=2,
        requester_user_id=1,
        requester_role="USER",
        otp_code=None,
    )

    with pytest.raises(ForbiddenError):
        service.to_execute(command)


def test_delete_user_not_found(service, mocker):
    mocker.patch(
        "app.domain.rules.user_rules.UserRules.get_and_validate_user_to_delete",
        side_effect=NotFoundError("Usuário não encontrado"),
    )

    command = DeleteUserCommand(
        user_id=99,
        requester_user_id=1,
        requester_role="ADMIN",
        otp_code=None,
    )

    with pytest.raises(NotFoundError):
        service.to_execute(command)


def test_self_delete_without_otp_fails(service, mocker, user):
    mocker.patch(
        "app.domain.rules.user_rules.UserRules.get_and_validate_user_to_delete",
        return_value=user,
    )

    mocker.patch(
        "app.domain.rules.user_rules.UserRules.validate_user_cannot_view_others",
        return_value=None,
    )

    mocker.patch(
        "app.domain.rules.user_rules.UserRules.validate_self_delete_otp",
        side_effect=ForbiddenError("OTP obrigatório"),
    )

    command = DeleteUserCommand(
        user_id=1,
        requester_user_id=1,
        requester_role="USER",
        otp_code=None,
    )

    with pytest.raises(ForbiddenError):
        service.to_execute(command)


def test_self_delete_with_invalid_otp_fails(service, mocker, user):
    mocker.patch(
        "app.domain.rules.user_rules.UserRules.get_and_validate_user_to_delete",
        return_value=user,
    )

    mocker.patch(
        "app.domain.rules.user_rules.UserRules.validate_user_cannot_view_others",
        return_value=None,
    )

    mocker.patch(
        "app.domain.rules.user_rules.UserRules.validate_self_delete_otp",
        side_effect=ForbiddenError("OTP inválido"),
    )

    command = DeleteUserCommand(
        user_id=1,
        requester_user_id=1,
        requester_role="USER",
        otp_code="000000",
    )

    with pytest.raises(ForbiddenError):
        service.to_execute(command)
