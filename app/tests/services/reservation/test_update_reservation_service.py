# run: pytest .\app\tests\services\reservation\test_update_reservation_service.py -s -v
import pytest
from datetime import date, time

from app.infrastructure.extensions import db
from app.domains.entities.table import Table
from app.domains.entities.reservation import Reservation
from app.domains.exceptions import ConflictError, NotFoundError
from app.application.services.reservation.update_reservation_service import UpdateReservationsService


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

    service = UpdateReservationsService(data, reservation.id, db_session)
    updated = service.to_execute()

    updated_from_db = db_session.get(Reservation, reservation.id)

    assert updated_from_db is not None
    assert updated_from_db.people_quantity == 3
    assert updated_from_db.booking_date == date.today()
    assert updated_from_db.initial_time == time(12, 0)
    assert updated_from_db.final_time == time(13, 0)


def test_update_reservation_not_found(db_session):
    data = {
        "people_quantity": 2,
    }

    service = UpdateReservationsService(data, reservation_id=999, session=db_session)
    with pytest.raises(NotFoundError) as error:
        service.to_execute()

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
    db_session.add(conflicting)
    db_session.commit()

    data = {
        "initial_time": time(12, 30),
        "final_time": time(13, 30),
    }

    service = UpdateReservationsService(data, reservation.id, db_session)
    with pytest.raises(ConflictError) as error:
        service.to_execute()

    assert "Já existe reserva agendada para esse horario!" in str(error.value)


def test_update_reservation_exceeds_table_capacity(db_session, table, reservation):
    data = {
        "people_quantity": 10,
    }

    service = UpdateReservationsService(data, reservation.id, db_session)
    with pytest.raises(ConflictError) as error:
        service.to_execute()

    assert "Quantidade de pessoas acima da capacidade" in str(error.value)
