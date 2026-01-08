# pytest .\app\tests\services\reservation\test_read_reservation_sevice.py -s -v

from datetime import date, time
import pytest

from app.exceptions import NotFoundError
from app.extensions import db
from app.models.reservation import Reservation
from app.models.table import Table

from app.services.reservation.create_reservation_service import (
    create_reservation_service,
)
from app.services.reservation.read_reservation_service import get_reservation_service


@pytest.fixture
def table(db_session):
    table = Table(
        table_number=1,
        people_capacity=4,
        status="Available",
    )
    db.session.add(table)
    db.session.commit()
    return table


@pytest.fixture
def reservation(db_session, table):
    data = {
        "client_name": "João",
        "people_quantity": 2,
        "table_number": 1,
        "booking_date": date.today(),
        "initial_time": time(16, 0),
        "final_time": time(17, 0),
    }

    create_reservation_service(data)

    reservation = Reservation.query.first()

    db.session.add(reservation)
    db.session.commit()
    return reservation


def test_read_reservation_success(db_session, reservation):
    reservation = get_reservation_service(reservation.id)

    assert reservation["client_name"] == "João"
    assert reservation["people_quantity"] == 2
    assert reservation["table_number"] == 1
    assert reservation["booking_date"] == date.today()
    assert time.fromisoformat(reservation["initial_time"]) == time(16, 0)
    assert time.fromisoformat(reservation["final_time"]) == time(17, 0, 0)


def test_read_reservation_not_found(db_session):

    with pytest.raises(NotFoundError) as error:
        get_reservation_service(1)

    assert "Reserva não encontrada" in str(error.value)
