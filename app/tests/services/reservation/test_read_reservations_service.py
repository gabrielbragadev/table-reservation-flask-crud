# pytest .\app\tests\services\reservation\test_read_reservations_service.py -s -v

from datetime import date, time
import pytest

from app.domains.exceptions import NotFoundError
from app.domains.entities.reservation import Reservation
from app.domains.entities.table import Table

from app.application.services.reservation.create_reservation_service import (
    CreateReservationService,
)
from app.application.services.reservation.read_reservations_service import (
    GetReservationsService,
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
def reservation_one_fixture(db_session, table):
    data_reservation_one = {
        "client_name": "João",
        "people_quantity": 2,
        "table_number": 1,
        "booking_date": date.today(),
        "initial_time": time(16, 0),
        "final_time": time(17, 0),
    }

    service = CreateReservationService(data_reservation_one, db_session)
    service.to_execute()

    return (
        db_session.query(Reservation)
        .filter_by(client_name=data_reservation_one["client_name"])
        .first()
    )


@pytest.fixture
def reservation_two_fixture(db_session, table):
    data_reservation_two = {
        "client_name": "Matheus",
        "people_quantity": 2,
        "table_number": 1,
        "booking_date": date.today(),
        "initial_time": time(20, 0),
        "final_time": time(21, 0),
    }

    service = CreateReservationService(data_reservation_two, db_session)
    service.to_execute()

    return (
        db_session.query(Reservation)
        .filter_by(client_name=data_reservation_two["client_name"])
        .first()
    )


def test_read_reservations_success(
    db_session, reservation_one_fixture, reservation_two_fixture
):
    service = GetReservationsService(db_session)
    reservations = service.to_execute()

    assert reservations[0]["client_name"] == reservation_one_fixture.client_name
    assert reservations[0]["people_quantity"] == reservation_one_fixture.people_quantity
    assert reservations[0]["table_number"] == reservation_one_fixture.table_number
    assert reservations[0]["booking_date"] == reservation_one_fixture.booking_date
    assert (
        time.fromisoformat(reservations[0]["initial_time"])
        == reservation_one_fixture.initial_time
    )
    assert (
        time.fromisoformat(reservations[0]["final_time"])
        == reservation_one_fixture.final_time
    )

    assert reservations[1]["client_name"] == reservation_two_fixture.client_name
    assert reservations[1]["people_quantity"] == reservation_two_fixture.people_quantity
    assert reservations[1]["table_number"] == reservation_two_fixture.table_number
    assert reservations[1]["booking_date"] == reservation_two_fixture.booking_date
    assert (
        time.fromisoformat(reservations[1]["initial_time"])
        == reservation_two_fixture.initial_time
    )
    assert (
        time.fromisoformat(reservations[1]["final_time"])
        == reservation_two_fixture.final_time
    )


def test_read_reservations_not_found(db_session):
    service = GetReservationsService(db_session)

    with pytest.raises(NotFoundError) as error:
        service.to_execute()

    assert "Nenhum registro encontrado" in str(error.value)
