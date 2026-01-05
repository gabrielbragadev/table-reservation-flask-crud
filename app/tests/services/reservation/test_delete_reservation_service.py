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
        "initial_time": time(18, 0),
        "final_time": time(20, 0),
    }

    create_reservation_service(data, user_authenticated=True)

    reservation = Reservation.query.first()

    db.session.add(reservation)
    db.session.commit()
    return reservation


def test_delete_reservation_success(db_session, reservation, table):
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


"""@pytest.fixture
def table(db_session):
    table = Table(
        table_number=1,
        people_capacity=4,
        status="available",
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
        "initial_time": time(18, 0),
        "final_time": time(20, 0),
    }

    create_reservation_service(data, user_authenticated=True)

    reservation = Reservation.query.first()

    assert reservation is not None
    assert reservation.client_name == "João"
    assert reservation.people_quantity == 2
    assert reservation.table_number == 1
    assert reservation.booking_date == date.today()
    assert reservation.initial_time == time(18, 0)
    assert reservation.final_time == time(20, 0)


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
        create_reservation_service(data, user_authenticated=True)

    assert "Mesa não encontrada" in str(error.value)


def test_create_reservation_unauthenticated_user(db_session, table):
    existing = Reservation(
        client_name="Carlos",
        people_quantity=2,
        table_number=1,
        booking_date=date.today(),
        initial_time=time(14, 0),
        final_time=time(16, 0),
    )
    db.session.add(existing)
    db.session.commit()

    data = {
        "client_name": "Ana",
        "people_quantity": 2,
        "table_number": 1,
        "booking_date": date.today(),
        "initial_time": time(18, 0),
        "final_time": time(20, 0),
    }

    with pytest.raises(UnauthorizedError) as error:
        create_reservation_service(data, user_authenticated=False)

    assert "Usuário precisa estar autenticado" in str(error.value)


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
        create_reservation_service(data, user_authenticated=True)

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
        create_reservation_service(data, user_authenticated=True)

    assert "Quantidade de pessoas acima da capacidade" in str(error.value)
"""
