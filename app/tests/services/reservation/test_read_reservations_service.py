# pytest .\app\tests\services\reservation\test_read_reservations_service.py -s -v

from datetime import date, time
import pytest

from app.exceptions import NotFoundError
from app.extensions import db
from app.models.reservation import Reservation
from app.models.table import Table

from app.services.reservation.create_reservation_service import (
    create_reservation_service,
)
from app.services.reservation.read_reservations_service import get_reservations_service


@pytest.fixture
def table(db_session):
    table = Table(
        table_number=1,
        people_capacity=4,
    )
    db.session.add(table)
    db.session.commit()
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

    create_reservation_service(data_reservation_one)

    reservation_one = Reservation.query.filter_by(
        client_name=data_reservation_one["client_name"]
    ).first()

    db.session.add(reservation_one)
    db.session.commit()

    return reservation_one


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

    create_reservation_service(data_reservation_two)

    reservation_two = Reservation.query.filter_by(
        client_name=data_reservation_two["client_name"]
    ).first()

    db.session.add(reservation_two)
    db.session.commit()

    return reservation_two


def test_read_reservations_success(
    db_session, reservation_one_fixture, reservation_two_fixture
):
    reservations = get_reservations_service()

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
        time.fromisoformat(reservations[0]["initial_time"])
        == reservation_one_fixture.initial_time
    )
    assert (
        time.fromisoformat(reservations[0]["final_time"])
        == reservation_one_fixture.final_time
    )


def test_read_reservations_not_found(db_session):
    with pytest.raises(NotFoundError) as error:
        get_reservations_service()

    assert "Nenhum registro encontrado" in str(error.value)
