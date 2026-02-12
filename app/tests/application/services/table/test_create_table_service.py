# pytest ./app/tests/application/services/table/test_create_table_service.py -s -v

import pytest
from unittest.mock import Mock

from app.application.services.table.create_table_service import CreateTableService
from app.application.commands.table.create_table_command import CreateTableCommand
from app.domain.entities.table import Table
from app.domain.exceptions import ConflictError, ForbiddenError


# =========================
# FIXTURES
# =========================

@pytest.fixture
def table_repository():
    return Mock()


@pytest.fixture
def unit_of_work():
    uow = Mock()
    uow.commit = Mock()
    return uow


@pytest.fixture
def service(table_repository, unit_of_work):
    return CreateTableService(
        table_repository=table_repository,
        unit_of_work=unit_of_work,
    )


def make_command(table_number=10, capacity=4, role="ADMIN"):
    data = Mock()
    data.table_number = table_number
    data.people_capacity = capacity

    return CreateTableCommand(
        data=data,
        requester_role=role,
    )


# =========================
# TESTES
# =========================

def test_should_create_table_successfully_when_user_is_admin(
    service,
    table_repository,
    unit_of_work,
    mocker,
):
    # arrange
    mocker.patch(
        "app.domain.rules.user_rules.UserRules.validate_user_role_permission",
        return_value=None,
    )

    mocker.patch(
        "app.domain.rules.table_rules.TableRules.validate_table_number",
        return_value=None,
    )

    command = make_command()

    # act
    result = service.to_execute(command)

    # assert
    assert isinstance(result, Table)
    assert result.table_number == 10
    assert result.people_capacity == 4

    table_repository.save.assert_called_once()
    unit_of_work.commit.assert_called_once()


def test_should_raise_forbidden_error_when_user_is_not_admin(
    service,
    mocker,
):
    # arrange
    mocker.patch(
        "app.domain.rules.user_rules.UserRules.validate_user_role_permission",
        side_effect=ForbiddenError("Ação permitida apenas para administradores."),
    )

    command = make_command(role="USER")

    # act / assert
    with pytest.raises(ForbiddenError):
        service.to_execute(command)


def test_should_raise_conflict_error_when_table_number_already_exists(
    service,
    mocker,
):
    # arrange
    mocker.patch(
        "app.domain.rules.user_rules.UserRules.validate_user_role_permission",
        return_value=None,
    )

    mocker.patch(
        "app.domain.rules.table_rules.TableRules.validate_table_number",
        side_effect=ConflictError("Já existe uma mesa cadastrada com esse número."),
    )

    command = make_command(table_number=10)

    # act / assert
    with pytest.raises(ConflictError):
        service.to_execute(command)
