# pytest .\app\tests\application\services\auth\test_login_service.py -s -v
import pytest
from unittest.mock import Mock, patch

from app.application.services.auth.login_service import UserLoginService
from app.application.commands.auth.user_login_command import UserLoginCommand
from app.application.dtos.auth.user_login_dto import UserLoginDTO

from app.domain.entities.user import User
from app.domain.exceptions import UnauthorizedError, NotFoundError


# ---------- FIXTURES ----------

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
def fake_request():
    return Mock()


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


# ---------- TESTES ----------

@patch("app.domain.rules.auth_rules.AuthRules.has_active_session")
@patch("app.domain.rules.auth_rules.AuthRules.resolve_user_by_username")
def test_user_login_success(
    mock_resolve_user,
    mock_has_active_session,
    service,
    command,
    fake_request,
    bcrypt_handler,
    flask_login_handler,
    user,
):
    mock_resolve_user.return_value = user

    result = service.user_login(command, fake_request)

    mock_has_active_session.assert_called_once_with(fake_request)
    mock_resolve_user.assert_called_once_with(
        service._UserLoginService__user_repository,
        "gabri",
    )
    bcrypt_handler.verify_hash.assert_called_once_with(user, b"123456")
    flask_login_handler.login.assert_called_once_with(user)

    assert result == user


@patch("app.domain.rules.auth_rules.AuthRules.has_active_session")
@patch("app.domain.rules.auth_rules.AuthRules.resolve_user_by_username")
def test_user_login_user_not_found(
    mock_resolve_user,
    mock_has_active_session,
    service,
    command,
    fake_request,
):
    mock_resolve_user.side_effect = NotFoundError("Usuário não encontrado")

    with pytest.raises(NotFoundError):
        service.user_login(command, fake_request)

    mock_has_active_session.assert_called_once_with(fake_request)


@patch("app.domain.rules.auth_rules.AuthRules.has_active_session")
@patch("app.domain.rules.auth_rules.AuthRules.resolve_user_by_username")
def test_user_login_invalid_password(
    mock_resolve_user,
    mock_has_active_session,
    service,
    command,
    fake_request,
    bcrypt_handler,
    flask_login_handler,
    user,
):
    mock_resolve_user.return_value = user
    bcrypt_handler.verify_hash.return_value = False

    with pytest.raises(UnauthorizedError) as exc:
        service.user_login(command, fake_request)

    assert "Credenciais Inválidas" in str(exc.value)

    flask_login_handler.login.assert_not_called()


@patch("app.domain.rules.auth_rules.AuthRules.has_active_session")
@patch("app.domain.rules.auth_rules.AuthRules.resolve_user_by_username")
def test_flask_login_not_called_when_password_invalid(
    mock_resolve_user,
    mock_has_active_session,
    service,
    command,
    fake_request,
    bcrypt_handler,
    flask_login_handler,
    user,
):
    mock_resolve_user.return_value = user
    bcrypt_handler.verify_hash.return_value = False

    with pytest.raises(UnauthorizedError):
        service.user_login(command, fake_request)

    flask_login_handler.login.assert_not_called()
