# run: pytest .\app\tests\\services\reservation\test_create_reservation_service.py -s -v
import pytest
from datetime import date, time

from app.domains.entities.table import Table
from app.domains.entities.reservation import Reservation
from app.domains.exceptions import ConflictError
from app.application.services.reservation.create_reservation_service import CreateReservationService


@pytest.fixture
def table(db_session):
    table = Table(
        table_number=1,
        people_capacity=4,
    )
    db_session.add(table)
    db_session.commit()
    return table


def test_create_reservation_success(db_session, table):
    data = {
        "client_name": "João",
        "people_quantity": 2,
        "table_number": 1,
        "booking_date": date.today(),
        "initial_time": time(10, 30),
        "final_time": time(11, 50),
    }

    service = CreateReservationService(data, db_session)
    reservation = service.to_execute()

    saved = db_session.query(Reservation).first()

    assert saved is not None
    assert saved.id == reservation.id
    assert saved.client_name == "João"
    assert saved.people_quantity == 2
    assert saved.table_number == 1
    assert saved.booking_date == date.today()
    assert saved.initial_time == time(10, 30)
    assert saved.final_time == time(11, 50)
    assert saved.status == "active"


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
        service = CreateReservationService(data, db_session)
        service.to_execute()

    assert "Mesa não encontrada" in str(error.value)


def test_create_reservation_time_conflict(db_session, table):
    existing = Reservation(
        client_name="Pedro",
        people_quantity=2,
        table_number=1,
        booking_date=date.today(),
        initial_time=time(18, 0),
        final_time=time(20, 0),
        status="active",
    )
    db_session.add(existing)
    db_session.commit()

    data = {
        "client_name": "Lucas",
        "people_quantity": 2,
        "table_number": 1,
        "booking_date": date.today(),
        "initial_time": time(19, 0),
        "final_time": time(21, 0),
    }

    with pytest.raises(ConflictError) as error:
        service = CreateReservationService(data, db_session)
        service.to_execute()

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
        service = CreateReservationService(data, db_session)
        service.to_execute()

    assert "Quantidade de pessoas acima da capacidade" in str(error.value)
