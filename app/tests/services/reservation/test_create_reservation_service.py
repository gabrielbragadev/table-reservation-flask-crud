# run: pytest .\app\tests\\services\reservation\test_create_reservation_service.py -s -v

import pytest
from datetime import date, time

from app.extensions import db
from app.models.table import Table
from app.models.reservation import Reservation
from app.exceptions import ConflictError
from app.services.reservation.create_reservation_service import (
    create_reservation_service,
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


def test_create_reservation_success(db_session, table):
    data = {
        "client_name": "João",
        "people_quantity": 2,
        "table_number": 1,
        "booking_date": date.today(),
        "initial_time": time(15, 50),
        "final_time": time(16, 50),
    }

    create_reservation_service(data)

    reservation = Reservation.query.first()

    assert reservation is not None
    assert reservation.client_name == "João"
    assert reservation.people_quantity == 2
    assert reservation.table_number == 1
    assert reservation.booking_date == date.today()
    assert reservation.initial_time == time(15, 50)
    assert reservation.final_time == time(16, 50)
    assert table.status == "Occupied"


def test_create_reservation_table_not_found(db_session):
    data = {
        "client_name": "Maria",
        "people_quantity": 2,
        "table_number": 999,
        "booking_date": date.today(),
        "initial_time": time(18, 0),
        "final_time": time(20, 0),
    }

    with pytest.raises(ValueError) as error:
        create_reservation_service(data)

    assert "Mesa não encontrada" in str(error.value)


def test_create_reservation_time_conflict(db_session, table):
    existing = Reservation(
        client_name="Pedro",
        people_quantity=2,
        table_number=1,
        booking_date=date.today(),
        initial_time=time(18, 0),
        final_time=time(20, 0),
    )
    db.session.add(existing)
    db.session.commit()

    data = {
        "client_name": "Lucas",
        "people_quantity": 2,
        "table_number": 1,
        "booking_date": date.today(),
        "initial_time": time(19, 0),
        "final_time": time(21, 0),
    }

    with pytest.raises(ConflictError) as error:
        create_reservation_service(data)

    assert "Já existe reserva agendada para esse horario!" in str(error.value)


def test_create_reservation_exceeds_table_capacity(db_session, table):
    data = {
        "client_name": "Rafael",
        "people_quantity": 10,
        "table_number": 1,
        "booking_date": date.today(),
        "initial_time": time(18, 0),
        "final_time": time(20, 0),
    }

    with pytest.raises(ConflictError) as error:
        create_reservation_service(data)

    assert "Quantidade de pessoas acima da capacidade" in str(error.value)
