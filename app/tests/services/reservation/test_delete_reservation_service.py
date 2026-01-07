# run: pytest .\app\tests\services\reservation\test_delete_reservation_service.py -s -v

from datetime import date, time
import pytest

from app.extensions import db
from app.models.reservation import Reservation
from app.models.table import Table
from app.exceptions import NotFoundError
from app.services.reservation.create_reservation_service import (
    create_reservation_service,
)
from app.services.reservation.delete_reservation_service import (
    delete_reservation_service,
)


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


def test_delete_reservation_success(db_session, reservation, table):
    print(reservation.table.status)

    mock_id = reservation.id
    delete_reservation_service(mock_id)

    reservation = Reservation.query.filter_by(id=mock_id).first()

    assert reservation is None
    assert table.status == "Available"


def test_delete_reservation_not_found(db_session):
    mock_id = 2

    with pytest.raises(NotFoundError) as error:
        delete_reservation_service(mock_id)

    assert "Reserva não encontrada" in str(error.value)
