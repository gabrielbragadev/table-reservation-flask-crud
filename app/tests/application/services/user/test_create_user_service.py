# pytest .\app\tests\application\services\user\test_create_user_service.py -s -v

import pytest
from unittest.mock import Mock

from app.application.services.user.create_user_service import CreateUserService
from app.application.commands.user.create_user_command import CreateUserCommand
from app.domain.entities.user import User
from app.domain.exceptions import (
    UnauthorizedError,
    ForbiddenError,
    ConflictError,
)


@pytest.fixture
def user_repository():
    return Mock()


@pytest.fixture
def flask_login_handler():
    return Mock()


@pytest.fixture
def unit_of_work():
    uow = Mock()
    uow.commit = Mock()
    return uow


@pytest.fixture
def create_user_command():
    command = Mock(spec=CreateUserCommand)
    command.requester_role = "admin"

    command.data = Mock()
    command.data.username = "john"
    command.data.email = "john@email.com"
    command.data.password = "123456"
    command.data.role = "user"

    return command


@pytest.fixture
def service(user_repository, flask_login_handler, unit_of_work):
    return CreateUserService(
        user_repository=user_repository,
        flask_login_handler=flask_login_handler,
        unit_of_work=unit_of_work,
    )


def test_should_create_user_successfully(
    service,
    user_repository,
    flask_login_handler,
    unit_of_work,
    create_user_command,
):
    user_repository.find_all.return_value = []
    flask_login_handler.find_current_user_is_authenticated.return_value = True
    user_repository.find_by_username.return_value = None
    user_repository.find_by_email.return_value = None

    user = service.to_execute(create_user_command)

    assert isinstance(user, User)
    assert user.username == "john"
    assert user.email == "john@email.com"

    user_repository.save.assert_called_once()
    unit_of_work.commit.assert_called_once()


def test_should_not_create_user_if_users_exist_and_not_authenticated(
    service,
    user_repository,
    flask_login_handler,
    create_user_command,
):
    user_repository.find_all.return_value = [Mock()]
    flask_login_handler.find_current_user_is_authenticated.return_value = False

    with pytest.raises(UnauthorizedError):
        service.to_execute(create_user_command)


def test_should_not_create_user_if_requester_is_not_admin(
    service,
    user_repository,
    flask_login_handler,
    create_user_command,
):
    user_repository.find_all.return_value = []
    flask_login_handler.find_current_user_is_authenticated.return_value = True
    create_user_command.requester_role = "user"

    with pytest.raises(ForbiddenError):
        service.to_execute(create_user_command)


def test_should_not_create_user_if_username_already_exists(
    service,
    user_repository,
    flask_login_handler,
    create_user_command,
):
    user_repository.find_all.return_value = []
    flask_login_handler.find_current_user_is_authenticated.return_value = True
    user_repository.find_by_username.return_value = [Mock()]
    user_repository.find_by_email.return_value = None

    with pytest.raises(ConflictError):
        service.to_execute(create_user_command)


def test_should_not_create_user_if_email_already_exists(
    service,
    user_repository,
    flask_login_handler,
    create_user_command,
):
    user_repository.find_all.return_value = []
    flask_login_handler.find_current_user_is_authenticated.return_value = True
    user_repository.find_by_username.return_value = None
    user_repository.find_by_email.return_value = [Mock()]

    with pytest.raises(ConflictError):
        service.to_execute(create_user_command)
