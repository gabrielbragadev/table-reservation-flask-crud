# pytest .\app\tests\application\services\reservation\test_read_reservation_service.py -s -v

import pytest
from unittest.mock import Mock, patch

from app.application.services.reservation.read_reservation_service import (
    GetReservationService,
)
from app.application.commands.reservation.read_reservation_command import (
    ReadReservationCommand,
)
from app.domain.exceptions import NotFoundError


@pytest.fixture
def reservation():
    reservation = Mock()
    reservation.booking_date = "2026-01-20"
    reservation.client_name = "Gabriel"
    reservation.initial_time = "18:00"
    reservation.final_time = "20:00"
    reservation.people_quantity = 4
    reservation.table_number = 10
    reservation.status = "CONFIRMED"
    return reservation


@pytest.fixture
def reservation_repository(reservation):
    repo = Mock()
    repo.find_by_id.return_value = reservation
    return repo


@pytest.fixture
def command():
    command = Mock(spec=ReadReservationCommand)
    command.reservation_id = 1
    command.requester_role = "ADMIN"
    command.requester_user_id = 1
    return command


@pytest.fixture
def service(reservation_repository):
    return GetReservationService(reservation_repository)


@patch(
    "app.domain.rules.reservation_rules.ReservationRules.check_permission_for_modification"
)
def test_get_reservation_success(
    mock_check_permission,
    service,
    command,
    reservation_repository,
    reservation,
):
    result = service.to_execute(command)

    mock_check_permission.assert_called_once_with(
        command.requester_role,
        command.reservation_id,
        command.requester_user_id,
    )

    reservation_repository.find_by_id.assert_called_once_with(
        command.reservation_id
    )

    assert result == {
        "booking_date": reservation.booking_date,
        "client_name": reservation.client_name,
        "initial_time": reservation.initial_time,
        "final_time": reservation.final_time,
        "people_quantity": reservation.people_quantity,
        "table_number": reservation.table_number,
        "status": reservation.status,
    }


@patch(
    "app.domain.rules.reservation_rules.ReservationRules.check_permission_for_modification"
)
def test_get_reservation_not_found(
    mock_check_permission,
    service,
    command,
    reservation_repository,
):
    reservation_repository.find_by_id.return_value = None

    with pytest.raises(NotFoundError) as exc:
        service.to_execute(command)

    assert "Reserva não encontrada" in str(exc.value)

    reservation_repository.find_by_id.assert_called_once_with(
        command.reservation_id
    )
