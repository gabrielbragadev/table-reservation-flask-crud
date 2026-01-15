# pytest .\app\tests\application\services\reservation\test_update_reservation_service.py -s -v
import pytest
from unittest.mock import Mock
from datetime import date, time

from app.application.services.reservation.update_reservation_service import (
    UpdateReservationsService,
)
from app.application.commands.reservation.update_reservation_command import (
    UpdateReservationCommand,
)
from app.application.dtos.reservation.update_reservation_dto import (
    UpdateReservationDTO,
)
from app.domain.entities.reservation import Reservation
from app.domain.entities.table import Table
from app.domain.exceptions import (
    NotFoundError,
    ForbiddenError,
    ConflictError,
)


# ------------------------
# FIXTURES
# ------------------------


@pytest.fixture
def reservation():
    return Reservation(
        id=1,
        client_name="Gabriel",
        people_quantity=2,
        table_number=10,
        booking_date=date(2026, 1, 20),
        initial_time=time(19, 0),
        final_time=time(20, 0),
        status="active",
    )


@pytest.fixture
def service_mocks():
    return {
        "reservation_repo": Mock(),
        "conflict_checker": Mock(),
        "table_provider": Mock(),
        "uow": Mock(),
    }


def make_service(mocks):
    return UpdateReservationsService(
        reservation_repository=mocks["reservation_repo"],
        conflict_checker=mocks["conflict_checker"],
        reservation_table_provider=mocks["table_provider"],
        unit_of_work=mocks["uow"],
    )


# ------------------------
# TESTS
# ------------------------


def test_update_reservation_success(reservation, service_mocks):
    service_mocks["reservation_repo"].find_by_id.return_value = reservation
    service_mocks["conflict_checker"].exists.return_value = False
    service_mocks["table_provider"].get_table_from_reservation.return_value = Table(
        table_number=12,
        people_capacity=4,
    )

    service = make_service(service_mocks)

    dto = UpdateReservationDTO(
        table_number=12,
        booking_date=date(2026, 1, 21),
        people_quantity=3,
        initial_time=time(20, 0),
        final_time=time(21, 0),
    )

    command = UpdateReservationCommand(
        reservation_id=1,
        requester_user_id=1,
        requester_role="admin",
        dto=dto,
    )

    updated = service.to_execute(command)

    assert updated.table_number == 12
    assert updated.booking_date == date(2026, 1, 21)
    assert updated.people_quantity == 3
    assert updated.initial_time == time(20, 0)
    assert updated.final_time == time(21, 0)

    service_mocks["uow"].commit.assert_called_once()


def test_update_reservation_not_found(service_mocks):
    service_mocks["reservation_repo"].find_by_id.return_value = None

    service = make_service(service_mocks)

    dto = UpdateReservationDTO(table_number=10)

    command = UpdateReservationCommand(
        reservation_id=99,
        requester_user_id=1,
        requester_role="admin",
        dto=dto,
    )

    with pytest.raises(NotFoundError):
        service.to_execute(command)

    service_mocks["uow"].commit.assert_not_called()


def test_update_reservation_forbidden(reservation, service_mocks):
    service_mocks["reservation_repo"].find_by_id.return_value = reservation

    service = make_service(service_mocks)

    dto = UpdateReservationDTO(table_number=11)

    command = UpdateReservationCommand(
        reservation_id=1,
        requester_user_id=999,  # não é dono
        requester_role="user",
        dto=dto,
    )

    with pytest.raises(ForbiddenError):
        service.to_execute(command)

    service_mocks["uow"].commit.assert_not_called()


def test_update_reservation_table_not_found(reservation, service_mocks):
    service_mocks["reservation_repo"].find_by_id.return_value = reservation
    service_mocks["table_provider"].get_table_from_reservation.side_effect = ValueError(
        "Mesa não encontrada"
    )

    service = make_service(service_mocks)

    dto = UpdateReservationDTO(table_number=99)

    command = UpdateReservationCommand(
        reservation_id=1,
        requester_user_id=1,
        requester_role="admin",
        dto=dto,
    )

    with pytest.raises(ValueError, match="Mesa não encontrada"):
        service.to_execute(command)


def test_update_reservation_time_conflict(reservation, service_mocks):
    service_mocks["reservation_repo"].find_by_id.return_value = reservation
    service_mocks["conflict_checker"].exists.return_value = True
    service_mocks["table_provider"].get_table_from_reservation.return_value = Table(
        table_number=10,
        people_capacity=4,
    )

    service = make_service(service_mocks)

    dto = UpdateReservationDTO(
        initial_time=time(19, 30),
        final_time=time(20, 30),
    )

    command = UpdateReservationCommand(
        reservation_id=1,
        requester_user_id=1,
        requester_role="admin",
        dto=dto,
    )

    with pytest.raises(ConflictError, match="Já existe reserva nesse horário"):
        service.to_execute(command)

    service_mocks["uow"].commit.assert_not_called()


def test_update_reservation_table_capacity_exceeded(reservation, service_mocks):
    service_mocks["reservation_repo"].find_by_id.return_value = reservation
    service_mocks["conflict_checker"].exists.return_value = False
    service_mocks["table_provider"].get_table_from_reservation.return_value = Table(
        table_number=10,
        people_capacity=2,
    )

    service = make_service(service_mocks)

    dto = UpdateReservationDTO(
        people_quantity=5,
    )

    command = UpdateReservationCommand(
        reservation_id=1,
        requester_user_id=1,
        requester_role="admin",
        dto=dto,
    )

    with pytest.raises(ConflictError):
        service.to_execute(command)

    service_mocks["uow"].commit.assert_not_called()


def test_update_reservation_partial_update(reservation, service_mocks):
    service_mocks["reservation_repo"].find_by_id.return_value = reservation
    service_mocks["conflict_checker"].exists.return_value = False
    service_mocks["table_provider"].get_table_from_reservation.return_value = Table(
        table_number=10,
        people_capacity=4,
    )

    service = make_service(service_mocks)

    dto = UpdateReservationDTO(
        people_quantity=4,
    )

    command = UpdateReservationCommand(
        reservation_id=1,
        requester_user_id=1,
        requester_role="admin",
        dto=dto,
    )

    updated = service.to_execute(command)

    assert updated.people_quantity == 4
    assert updated.table_number == 10  # manteve
    assert updated.booking_date == date(2026, 1, 20)  # manteve

    service_mocks["uow"].commit.assert_called_once()
