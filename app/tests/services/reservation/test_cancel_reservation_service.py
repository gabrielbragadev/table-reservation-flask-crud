# run: pytest .\app\tests\services\reservation\test_cancel_reservation_service.py -s -v

from datetime import date, time
import pytest

from app.models.reservation import Reservation
from app.models.table import Table
from app.exceptions import NotFoundError
from app.services.reservation.create_reservation_service import (
    create_reservation_service,
)
from app.services.reservation.cancel_reservation_service import (
    cancel_reservation_service,
)
from app.extensions import db


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

    create_reservation_service(data)
    return Reservation.query.first()


def test_cancel_reservation_service(db_session, reservation, table):
    reservation_id = reservation.id

    cancel_reservation_service(reservation_id)

    updated = db.session.get(Reservation, reservation_id)

    assert updated is not None

    assert updated.status == "cancelled"

    assert table.status == "available"


def test_cancel_reservation_not_found(db_session):
    with pytest.raises(NotFoundError) as error:
        cancel_reservation_service(999)

    assert "Reserva não encontrada" in str(error.value)
