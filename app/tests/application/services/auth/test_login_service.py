# pytest .\app\tests\application\services\auth\test_login_service.py -s -v

import pytest
from unittest.mock import Mock

from app.application.services.auth.login_service import UserLoginService
from app.application.commands.auth.user_login_command import UserLoginCommand
from app.application.dtos.auth.user_login_dto import UserLoginDTO

from app.domain.entities.user import User
from app.domain.exceptions import UnauthorizedError, NotFoundError


@pytest.fixture
def user():
    return User(
        id=1,
        username="gabri",
        email="gabri@email.com",
        password=b"$2b$12$hashedpassword",
        role="ADMIN",
    )


@pytest.fixture
def user_repository(user):
    repo = Mock()
    repo.find_by_username.return_value = user
    return repo


@pytest.fixture
def bcrypt_handler():
    bcrypt = Mock()
    bcrypt.verify_hash.return_value = True
    return bcrypt


@pytest.fixture
def flask_login_handler():
    handler = Mock()
    handler.login.return_value = None
    return handler


@pytest.fixture
def service(bcrypt_handler, user_repository, flask_login_handler):
    return UserLoginService(
        bcrypt_handler=bcrypt_handler,
        user_repository=user_repository,
        flask_login_handler=flask_login_handler,
    )


@pytest.fixture
def command():
    dto = UserLoginDTO(username="gabri", password=b"123456")
    return UserLoginCommand(dto=dto)


def test_user_login_success(
    service,
    command,
    user_repository,
    bcrypt_handler,
    flask_login_handler,
    user,
):
    result = service.user_login(command)

    user_repository.find_by_username.assert_called_once_with("gabri")
    bcrypt_handler.verify_hash.assert_called_once_with(user, b"123456")
    flask_login_handler.login.assert_called_once_with(user)

    assert result == user


def test_user_login_user_not_found(
    service,
    command,
    user_repository,
):
    user_repository.find_by_username.return_value = None

    with pytest.raises(NotFoundError) as exc:
        service.user_login(command)

    assert "Usuário não encontrado" in str(exc.value)


def test_user_login_invalid_password(
    service,
    command,
    bcrypt_handler,
    flask_login_handler,
):
    bcrypt_handler.verify_hash.return_value = False

    with pytest.raises(UnauthorizedError) as exc:
        service.user_login(command)

    assert "Credenciais Inválidas" in str(exc.value)

    flask_login_handler.login.assert_not_called()


def test_flask_login_not_called_when_password_is_invalid(
    service,
    command,
    bcrypt_handler,
    flask_login_handler,
):
    bcrypt_handler.verify_hash.return_value = False

    with pytest.raises(UnauthorizedError):
        service.user_login(command)

    flask_login_handler.login.assert_not_called()


def test_repository_called_with_correct_username(
    service,
    command,
    user_repository,
):
    service.user_login(command)

    user_repository.find_by_username.assert_called_once_with("gabri")
