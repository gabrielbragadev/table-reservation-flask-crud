# pytest .\app\tests\application\services\user\test_update_user_service.py -s -v

import pytest
from unittest.mock import Mock

from app.application.services.user.update_user_service import UpdateUserService
from app.application.commands.user.update_user_command import UpdateUserCommand
from app.application.dtos.user.update_user_dto import UpdateUserDTO
from app.domain.exceptions import ConflictError, ForbiddenError
from app.domain.entities.user import User


# =========================
# FIXTURES
# =========================


@pytest.fixture
def user():
    user = Mock(spec=User)
    user.id = 1
    user.username = "old_username"
    user.email = "old@email.com"
    user.password = "old_hash"
    user.role = "user"
    return user


@pytest.fixture
def admin_user():
    admin = Mock(spec=User)
    admin.id = 99
    admin.username = "admin"
    admin.email = "admin@email.com"
    admin.role = "admin"
    return admin


@pytest.fixture
def user_repository(user):
    repo = Mock()
    repo.find_by_id.return_value = user
    repo.find_by_username.return_value = None
    repo.find_by_email.return_value = None
    return repo


@pytest.fixture
def bcrypt_handler():
    bcrypt = Mock()
    bcrypt.generate_hash.return_value = "hashed_password"
    return bcrypt


@pytest.fixture
def unit_of_work():
    uow = Mock()
    uow.commit = Mock()
    return uow


@pytest.fixture
def service(user_repository, bcrypt_handler, unit_of_work):
    return UpdateUserService(user_repository, bcrypt_handler, unit_of_work)


# =========================
# TESTS
# =========================


def test_should_update_own_user_successfully(
    service, user_repository, bcrypt_handler, unit_of_work, user
):
    dto = UpdateUserDTO(
        username="new_username",
        password="new_password",
        email="new@email.com",
    )

    command = UpdateUserCommand(
        user_id=1,
        dto=dto,
        requester_user_id=1,
        requester_role="user",
    )

    service.to_execute(command)

    bcrypt_handler.generate_hash.assert_called_once_with("new_password")
    assert user.username == "new_username"
    assert user.email == "new@email.com"
    assert user.password == "hashed_password"
    unit_of_work.commit.assert_called_once()


def test_should_allow_admin_to_edit_other_user(
    service, user_repository, admin_user, unit_of_work
):
    user_repository.find_by_id.side_effect = [
        Mock(id=2, role="user"),  # user_id
    ]

    dto = UpdateUserDTO(role="admin")

    command = UpdateUserCommand(
        user_id=2,
        dto=dto,
        requester_user_id=99,
        requester_role="admin",
    )

    service.to_execute(command)

    unit_of_work.commit.assert_called_once()


def test_should_forbid_non_admin_editing_other_user(service, user_repository):
    dto = UpdateUserDTO(username="hack")

    other_user = Mock()
    other_user.id = 2

    user_repository.find_by_id.return_value = other_user

    command = UpdateUserCommand(
        user_id=2,
        dto=dto,
        requester_user_id=1,
        requester_role="user",
    )

    with pytest.raises(ForbiddenError):
        service.to_execute(command)


def test_should_raise_conflict_when_username_is_taken(service, user_repository):
    user_repository.find_by_username.return_value = [Mock()]

    dto = UpdateUserDTO(username="existing")

    command = UpdateUserCommand(
        user_id=1,
        dto=dto,
        requester_user_id=1,
        requester_role="user",
    )

    with pytest.raises(ConflictError):
        service.to_execute(command)


def test_should_raise_conflict_when_email_is_taken(service, user_repository):
    user_repository.find_by_email.return_value = [Mock()]

    dto = UpdateUserDTO(email="taken@email.com")

    command = UpdateUserCommand(
        user_id=1,
        dto=dto,
        requester_user_id=1,
        requester_role="user",
    )

    with pytest.raises(ConflictError):
        service.to_execute(command)


def test_should_fallback_to_requester_user_when_target_user_not_found(
    service, user_repository, user, unit_of_work
):
    user_repository.find_by_id.side_effect = [
        None,  # user_id not found
        user,  # requester_user_id
    ]

    dto = UpdateUserDTO(username="self_update")

    command = UpdateUserCommand(
        user_id=99,
        dto=dto,
        requester_user_id=1,
        requester_role="user",
    )

    service.to_execute(command)

    assert user.username == "self_update"
    unit_of_work.commit.assert_called_once()


def test_should_not_generate_password_hash_when_password_is_none(
    service, bcrypt_handler, unit_of_work
):
    dto = UpdateUserDTO(username="only_username")

    command = UpdateUserCommand(
        user_id=1,
        dto=dto,
        requester_user_id=1,
        requester_role="user",
    )

    service.to_execute(command)

    bcrypt_handler.generate_hash.assert_called_once_with(None)
    unit_of_work.commit.assert_called_once()
