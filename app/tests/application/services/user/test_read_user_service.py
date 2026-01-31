# pytest .\app\tests\application\services\user\test_read_user_service.py -s -v

import pytest
from unittest.mock import MagicMock, patch

from app.application.services.user.read_user_service import GetUserService
from app.application.commands.user.read_user_command import ReadUserCommand
from app.application.dtos.user.read_user_dto import ReadUserDTO
from app.domain.entities.user import User
from app.domain.exceptions import NotFoundError


# =========================
# FIXTURES
# =========================

@pytest.fixture
def user_repository_mock():
    return MagicMock()


@pytest.fixture
def service(user_repository_mock):
    return GetUserService(user_repository=user_repository_mock)


@pytest.fixture
def read_user_dto():
    return ReadUserDTO(
        user_id=1,
        username="gabriel",
        email="gabriel@email.com",
        role=1,
    )


# =========================
# TESTES
# =========================

def test_should_raise_exception_when_user_cannot_view_others(
    service, user_repository_mock, read_user_dto
):
    command = ReadUserCommand(
        user_id=2,
        requester_user_id=1,
        requester_role="USER",
        dto=read_user_dto,
    )

    with patch(
        "app.domain.rules.user_rules.UserRules.validate_user_cannot_view_others",
        side_effect=Exception("Sem permissão"),
    ):
        with pytest.raises(Exception, match="Sem permissão"):
            service.to_execute(command)

    user_repository_mock.find_by_id.assert_not_called()


def test_should_raise_not_found_error_when_user_does_not_exist(
    service, user_repository_mock, read_user_dto
):
    command = ReadUserCommand(
        user_id=1,
        requester_user_id=1,
        requester_role="USER",
        dto=read_user_dto,
    )

    user_repository_mock.find_by_id.return_value = None

    with patch(
        "app.domain.rules.user_rules.UserRules.validate_user_cannot_view_others"
    ):
        with pytest.raises(NotFoundError, match="Usuário não encontrado"):
            service.to_execute(command)

    user_repository_mock.find_by_id.assert_called_once_with(1)


def test_should_return_user_when_user_views_own_profile(
    service, user_repository_mock, read_user_dto
):
    user = MagicMock(spec=User)
    user.username = "gabriel"
    user.email = "gabriel@email.com"
    user.role = 1

    command = ReadUserCommand(
        user_id=1,
        requester_user_id=1,
        requester_role="USER",
        dto=read_user_dto,
    )

    user_repository_mock.find_by_id.return_value = user

    with patch(
        "app.domain.rules.user_rules.UserRules.validate_user_cannot_view_others"
    ):
        result = service.to_execute(command)

    assert result == {
        "username": "gabriel",
        "email": "gabriel@email.com",
        "role": 1,
    }

    user_repository_mock.find_by_id.assert_called_once_with(1)


def test_should_return_user_when_admin_views_other_user(
    service, user_repository_mock, read_user_dto
):
    user = MagicMock(spec=User)
    user.username = "gabriel"
    user.email = "gabriel@email.com"
    user.role = 1

    command = ReadUserCommand(
        user_id=2,
        requester_user_id=1,
        requester_role="ADMIN",
        dto=read_user_dto,
    )

    user_repository_mock.find_by_id.return_value = user

    with patch(
        "app.domain.rules.user_rules.UserRules.validate_user_cannot_view_others"
    ):
        result = service.to_execute(command)

    assert result == {
        "username": "gabriel",
        "email": "gabriel@email.com",
        "role": 1,
    }

    user_repository_mock.find_by_id.assert_called_once_with(2)
