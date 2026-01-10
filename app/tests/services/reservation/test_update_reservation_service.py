# run: pytest .\app\tests\services\reservation\test_update_reservation_service.py -s -v
import pytest
from datetime import date, time

from app.extensions import db
from app.models.table import Table
from app.models.reservation import Reservation
from app.exceptions import ConflictError, NotFoundError
from app.services.reservation.update_reservation_service import (
    update_reservation_service,
)


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
def reservation(db_session, table):
    reservation = Reservation(
        client_name="João",
        people_quantity=2,
        table_number=1,
        booking_date=date.today(),
        initial_time=time(10, 0),
        final_time=time(11, 0),
        status="active",
    )
    db.session.add(reservation)
    db.session.commit()
    return reservation


def test_update_reservation_success(db_session, table, reservation):
    data = {
        "people_quantity": 3,
        "booking_date": date.today(),
        "initial_time": time(12, 0),
        "final_time": time(13, 0),
    }

    update_reservation_service(data, reservation.id)

    updated = Reservation.query.get(reservation.id)

    assert updated is not None
    assert updated.people_quantity == 3
    assert updated.booking_date == date.today()
    assert updated.initial_time == time(12, 0)
    assert updated.final_time == time(13, 0)


def test_update_reservation_not_found(db_session):
    data = {
        "people_quantity": 2,
    }

    with pytest.raises(NotFoundError) as error:
        update_reservation_service(data, reservation_id=999)

    assert "Reserva não encontrada" in str(error.value)


def test_update_reservation_time_conflict(db_session, table, reservation):
    conflicting = Reservation(
        client_name="Maria",
        people_quantity=2,
        table_number=1,
        booking_date=date.today(),
        initial_time=time(12, 0),
        final_time=time(13, 0),
        status="active",
    )
    db.session.add(conflicting)
    db.session.commit()

    data = {
        "initial_time": time(12, 30),
        "final_time": time(13, 30),
    }

    with pytest.raises(ConflictError) as error:
        update_reservation_service(data, reservation.id)

    assert "Já existe reserva agendada para esse horario!" in str(error.value)


def test_update_reservation_exceeds_table_capacity(db_session, table, reservation):
    data = {
        "people_quantity": 10,
    }

    with pytest.raises(ConflictError) as error:
        update_reservation_service(data, reservation.id)

    assert "Quantidade de pessoas acima da capacidade" in str(error.value)
