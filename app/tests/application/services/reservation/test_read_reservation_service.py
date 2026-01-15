# pytest .\app\tests\application\services\reservation\test_read_reservation_service.py -s -v

import pytest
from unittest.mock import Mock

from app.application.services.reservation.read_reservation_service import (
    GetReservationService,
)
from app.application.commands.reservation.read_reservation_command import (
    ReadReservationCommand,
)
from app.domain.entities.reservation import Reservation
from app.domain.exceptions import NotFoundError, ForbiddenError


def test_get_reservation_success_admin():
    reservation_repo = Mock()

    service = GetReservationService(reservation_repository=reservation_repo)

    command = ReadReservationCommand(
        requester_role="admin",
        requester_user_id=1,
        dto=Mock(reservation_id=10),
    )

    reservation = Reservation(
        id=10,
        client_name="Gabriel",
        people_quantity=2,
        table_number=5,
        booking_date=None,
        initial_time=None,
        final_time=None,
        status="active",
    )

    reservation_repo.find_by_id.return_value = reservation

    result = service.to_execute(command)

    assert result == reservation
    reservation_repo.find_by_id.assert_called_once_with(10)


def test_get_reservation_not_found():
    reservation_repo = Mock()

    service = GetReservationService(reservation_repository=reservation_repo)

    command = ReadReservationCommand(
        requester_role="admin",
        requester_user_id=1,
        dto=Mock(reservation_id=999),
    )

    reservation_repo.find_by_id.return_value = None

    with pytest.raises(NotFoundError):
        service.to_execute(command)

    reservation_repo.find_by_id.assert_called_once_with(999)


def test_get_reservation_forbidden_for_non_owner():
    reservation_repo = Mock()

    service = GetReservationService(reservation_repository=reservation_repo)

    command = ReadReservationCommand(
        requester_role="user",
        requester_user_id=1,
        dto=Mock(reservation_id=10),
    )

    with pytest.raises(ForbiddenError):
        service.to_execute(command)

    reservation_repo.find_by_id.assert_not_called()
