# pytest .\app\tests\application\services\user\test_read_users_service.py -s -v

import pytest
from unittest.mock import MagicMock, patch

from app.application.services.user.read_users_service import GetUsersService
from app.application.commands.user.read_users_command import ReadUsersCommand
from app.domain.exceptions import NotFoundError, ForbiddenError
from app.domain.entities.user import User


@pytest.fixture
def user_repository_mock():
    return MagicMock()


@pytest.fixture
def service(user_repository_mock):
    return GetUsersService(user_repository=user_repository_mock)


def make_user(user_id=1, username="gabriel", email="g@email.com", role="USER"):
    user = MagicMock(spec=User)
    user.id = user_id
    user.username = username
    user.email = email
    user.role = role
    return user


def test_should_raise_not_found_error_when_no_users_exist(
    service, user_repository_mock
):
    user_repository_mock.find_all.return_value = None

    command = ReadUsersCommand(
        requester_role="admin",
        requester_user_id=1,
    )

    with pytest.raises(NotFoundError, match="Nenhum registro encontrado"):
        service.to_execute(command)

    user_repository_mock.find_all.assert_called_once()


def test_should_raise_forbidden_error_when_user_has_no_permission(
    service, user_repository_mock
):
    user_repository_mock.find_all.return_value = [
        make_user(),
        make_user(2, "ana"),
    ]

    command = ReadUsersCommand(
        requester_role="user",
        requester_user_id=1,
    )

    with patch(
        "app.domain.rules.user_rules.UserRules.validate_user_role_permission",
        side_effect=ForbiddenError(
            "Você não tem permissão para realizar esta ação."
        ),
    ):
        with pytest.raises(ForbiddenError):
            service.to_execute(command)


def test_should_return_users_dto_when_admin_requests_users(
    service, user_repository_mock
):
    users = [
        make_user(1, "gabriel", "g@email.com", "admin"),
        make_user(2, "ana", "ana@email.com", "user"),
    ]

    user_repository_mock.find_all.return_value = users

    command = ReadUsersCommand(
        requester_role="admin",
        requester_user_id=1,
    )

    with patch(
        "app.domain.rules.user_rules.UserRules.validate_user_role_permission",
        return_value=None,
    ):
        result = service.to_execute(command)

    assert result is not None
    assert len(result.users) == 2

    assert result.users[0].user_id == 1
    assert result.users[0].username == "gabriel"
    assert result.users[0].email == "g@email.com"
    assert result.users[0].role == "admin"

    assert result.users[1].user_id == 2
    assert result.users[1].username == "ana"
    assert result.users[1].email == "ana@email.com"
    assert result.users[1].role == "user"
