# run: pytest .\app\tests\services\reservation\test_cancel_reservation_service.py -s -v

from datetime import date, time
import pytest

from app.domains.entities.reservation import Reservation
from app.domains.entities.table import Table
from app.domains.exceptions import NotFoundError
from app.application.services.reservation.create_reservation_service import (
    CreateReservationService,
)
from app.application.services.reservation.cancel_reservation_service import (
    CancelReservationService,
)


@pytest.fixture
def table(db_session):
    table = Table(
        table_number=1,
        people_capacity=4,
    )
    db_session.add(table)
    db_session.commit()
    return table


@pytest.fixture
def reservation(db_session, table):
    data = {
        "client_name": "João",
        "people_quantity": 2,
        "table_number": 1,
        "booking_date": date.today(),
        "initial_time": time(23, 0),
        "final_time": time(23, 30),
    }

    service = CreateReservationService(data, db_session)
    service.to_execute()

    return db_session.query(Reservation).first()


def test_cancel_reservation_service(db_session, reservation):
    reservation_id = reservation.id

    service = CancelReservationService(reservation_id, db_session)
    updated = service.to_execute()

    assert updated is not None
    assert updated.status == "cancelled"


def test_cancel_reservation_not_found(db_session):
    service = CancelReservationService(999, db_session)

    with pytest.raises(NotFoundError) as error:
        service.to_execute()

    assert "Reserva não encontrada" in str(error.value)
