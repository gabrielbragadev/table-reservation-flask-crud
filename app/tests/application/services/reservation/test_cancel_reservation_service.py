# pytest .\app\tests\application\services\reservation\test_cancel_reservation_service.py -s -v
import pytest
from unittest.mock import Mock

from app.application.services.reservation.cancel_reservation_service import (
    CancelReservationService,
)
from app.application.commands.reservation.cancel_reservation_command import (
    CancelReservationCommand,
)
from app.domain.entities.reservation import Reservation
from app.domain.exceptions import ForbiddenError, NotFoundError


def test_cancel_reservation_success_as_admin():
    # Arrange
    reservation_repo = Mock()
    uow = Mock()

    service = CancelReservationService(
        reservation_repository=reservation_repo,
        unit_of_work=uow,
    )

    reservation = Reservation(
        id=1,
        client_name="Gabriel",
        status="active",
    )

    reservation_repo.find_by_id.return_value = reservation

    command = CancelReservationCommand(
        reservation_id=1,
        requester_user_id=999,
        requester_role="admin",
    )

    # Act
    result = service.to_execute(command)

    # Assert
    assert result.status == "cancelled"
    reservation_repo.save.assert_called_once_with(reservation)
    uow.commit.assert_called_once()


def test_cancel_reservation_forbidden_for_non_admin():
    # Arrange
    reservation_repo = Mock()
    uow = Mock()

    service = CancelReservationService(
        reservation_repository=reservation_repo,
        unit_of_work=uow,
    )

    command = CancelReservationCommand(
        reservation_id=10,
        requester_user_id=1,
        requester_role="user",
    )

    # Act / Assert
    with pytest.raises(ForbiddenError):
        service.to_execute(command)

    reservation_repo.find_by_id.assert_not_called()
    reservation_repo.save.assert_not_called()
    uow.commit.assert_not_called()


def test_cancel_reservation_not_found():
    # Arrange
    reservation_repo = Mock()
    uow = Mock()

    service = CancelReservationService(
        reservation_repository=reservation_repo,
        unit_of_work=uow,
    )

    reservation_repo.find_by_id.return_value = None

    command = CancelReservationCommand(
        reservation_id=999,
        requester_user_id=1,
        requester_role="admin",
    )

    # Act / Assert
    with pytest.raises(NotFoundError):
        service.to_execute(command)

    reservation_repo.save.assert_not_called()
    uow.commit.assert_not_called()

