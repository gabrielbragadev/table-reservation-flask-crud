# pytest .\app\tests\application\services\reservation\test_read_reservations_service.py -s -v

from datetime import date, time
import pytest
from unittest.mock import Mock

from app.application.services.reservation.read_reservations_service import (
    GetReservationsService,
)
from app.application.commands.reservation.read_reservations_command import (
    ReadReservationsCommand,
)
from app.application.dtos.reservation.read_reservation_dto import ReadReservationDTO
from app.application.dtos.reservation.read_reservations_dto import ReadReservationsDTO
from app.domain.entities.reservation import Reservation
from app.domain.exceptions import ForbiddenError, NotFoundError


def test_get_reservations_success():
    # Arrange
    reservation_repo = Mock()

    service = GetReservationsService(
        reservation_repository=reservation_repo
    )

    command = ReadReservationsCommand(
        requester_role="admin",
        requester_user_id=1,
    )

    reservation = Mock(spec=Reservation)
    reservation.reservation_id = 1
    reservation.client_name = "Gabriel"
    reservation.people_quantiry = 2
    reservation.table_number = 10
    reservation.booking_date = date(2026, 1, 20)
    reservation.initial_time = time(19, 0)
    reservation.final_time = time(20, 0)
    reservation.status = "active"

    reservation_repo.find_all.return_value = [reservation]

    # Act
    result = service.to_execute(command)

    # Assert
    assert isinstance(result, ReadReservationsDTO)
    assert len(result.reservations) == 1

    dto = result.reservations[0]
    assert dto.client_name == "Gabriel"
    assert dto.status == "active"

    reservation_repo.find_all.assert_called_once()




def test_get_reservations_not_found():
    reservation_repo = Mock()

    service = GetReservationsService(reservation_repo)

    command = ReadReservationsCommand(
        requester_role="admin",
        requester_user_id=1,
    )

    reservation_repo.find_all.return_value = []

    with pytest.raises(NotFoundError):
        service.to_execute(command)

    reservation_repo.find_all.assert_called_once()




def test_get_reservations_forbidden():
    reservation_repo = Mock()

    service = GetReservationsService(reservation_repo)

    command = ReadReservationsCommand(
        requester_role="user",
        requester_user_id=2,
    )

    with pytest.raises(ForbiddenError):
        service.to_execute(command)

    reservation_repo.find_all.assert_not_called()

