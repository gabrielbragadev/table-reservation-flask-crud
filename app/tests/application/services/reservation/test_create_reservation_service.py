# pytest .\app\tests\application\services\reservation\test_create_reservation_service.py -s -v

import pytest
from unittest.mock import Mock
from datetime import date, time

from app.application.services.reservation.create_reservation_service import (
    CreateReservationService,
)
from app.application.commands.reservation.create_reservation_command import (
    CreateReservationCommand,
)
from app.application.dtos.reservation.create_reservation_dto import (
    CreateReservationDTO,
)
from app.domain.entities.table import Table
from app.domain.exceptions import ConflictError, NotFoundError


def test_create_reservation_success():
    reservation_repo = Mock()
    conflict_checker = Mock()
    table_provider = Mock()
    uow = Mock()

    table_provider.get_table_from_reservation.return_value = Table(
        table_number=10,
        people_capacity=4,
    )

    conflict_checker.exists.return_value = False

    service = CreateReservationService(
        reservation_repository=reservation_repo,
        conflict_checker=conflict_checker,
        reservation_table_provider=table_provider,
        unit_of_work=uow,
    )

    dto = CreateReservationDTO(
        client_name="Gabriel",
        people_quantity=2,
        table_number=10,
        booking_date=date(2026, 1, 20),
        initial_time=time(19, 0),
        final_time=time(20, 0),
    )

    command = CreateReservationCommand(data=dto)

    reservation = service.to_execute(command)

    # comportamento
    table_provider.get_table_from_reservation.assert_called_once_with(10)
    conflict_checker.exists.assert_called_once()
    reservation_repo.save.assert_called_once()
    uow.commit.assert_called_once()

    # estado
    assert reservation.client_name == "Gabriel"
    assert reservation.people_quantity == 2
    assert reservation.table_number == 10
    assert reservation.status == "active"


def test_create_reservation_table_not_found():
    reservation_repo = Mock()
    conflict_checker = Mock()
    table_provider = Mock()
    uow = Mock()

    table_provider.get_table_from_reservation.side_effect = NotFoundError(
        message="Mesa não encontrada"
    )

    service = CreateReservationService(
        reservation_repository=reservation_repo,
        conflict_checker=conflict_checker,
        reservation_table_provider=table_provider,
        unit_of_work=uow,
    )

    dto = CreateReservationDTO(
        client_name="Gabriel",
        people_quantity=2,
        table_number=99,
        booking_date=date.today(),
        initial_time=time(19, 0),
        final_time=time(20, 0),
    )

    command = CreateReservationCommand(data=dto)

    with pytest.raises(NotFoundError):
        service.to_execute(command)

    reservation_repo.save.assert_not_called()
    uow.commit.assert_not_called()


def test_create_reservation_with_time_conflict():
    reservation_repo = Mock()
    conflict_checker = Mock()
    table_provider = Mock()
    uow = Mock()

    table_provider.get_table_from_reservation.return_value = Table(
        table_number=10,
        people_capacity=4,
    )

    conflict_checker.exists.return_value = True

    service = CreateReservationService(
        reservation_repository=reservation_repo,
        conflict_checker=conflict_checker,
        reservation_table_provider=table_provider,
        unit_of_work=uow,
    )

    dto = CreateReservationDTO(
        client_name="Gabriel",
        people_quantity=2,
        table_number=10,
        booking_date=date.today(),
        initial_time=time(19, 0),
        final_time=time(20, 0),
    )

    command = CreateReservationCommand(data=dto)

    with pytest.raises(ConflictError):
        service.to_execute(command)

    reservation_repo.save.assert_not_called()
    uow.commit.assert_not_called()


def test_create_reservation_table_capacity_exceeded():
    reservation_repo = Mock()
    conflict_checker = Mock()
    table_provider = Mock()
    uow = Mock()

    table_provider.get_table_from_reservation.return_value = Table(
        table_number=10,
        people_capacity=2,
    )

    conflict_checker.exists.return_value = False

    service = CreateReservationService(
        reservation_repository=reservation_repo,
        conflict_checker=conflict_checker,
        reservation_table_provider=table_provider,
        unit_of_work=uow,
    )

    dto = CreateReservationDTO(
        client_name="Gabriel",
        people_quantity=5,
        table_number=10,
        booking_date=date.today(),
        initial_time=time(19, 0),
        final_time=time(20, 0),
    )

    command = CreateReservationCommand(data=dto)

    with pytest.raises(ConflictError):
        service.to_execute(command)

    reservation_repo.save.assert_not_called()
    uow.commit.assert_not_called()
