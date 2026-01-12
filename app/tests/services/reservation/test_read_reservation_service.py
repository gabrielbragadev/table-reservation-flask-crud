# run: pytest .\app\tests\services\reservation\test_read_reservation_service.py -s -v

from datetime import date, time
import pytest

from app.exceptions import NotFoundError
from app.models.reservation import Reservation
from app.models.table import Table

from app.services.reservation.create_reservation_service import (
    CreateReservationService,
)
from app.services.reservation.read_reservation_service import GetReservationService


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
        "initial_time": time(21, 0),
        "final_time": time(22, 0),
    }

    service = CreateReservationService(data, db_session)
    service.to_execute()

    return db_session.query(Reservation).first()


def test_read_reservation_success(db_session, reservation, table):
    service = GetReservationService(reservation.id, db_session)
    reservation_data = service.to_execute(reservation.id)

    assert reservation_data["client_name"] == "João"
    assert reservation_data["people_quantity"] == 2
    assert reservation_data["table_number"] == 1
    assert reservation_data["booking_date"] == date.today()
    assert time.fromisoformat(reservation_data["initial_time"]) == time(21, 0)
    assert time.fromisoformat(reservation_data["final_time"]) == time(22, 0)

    assert reservation_data["table"]["status"] == "occupied"


def test_read_reservation_not_found(db_session):
    service = GetReservationService(999, db_session)

    with pytest.raises(NotFoundError) as error:
        service.to_execute(999)

    assert "Reserva não encontrada" in str(error.value)
