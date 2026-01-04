from datetime import date, time
from typing import Dict, List

from app.exceptions import ConflictError, UnauthorizedError
from app.extensions import db
from app.models.reservation import Reservation
from app.models.table import Table
from app.services.global_services.calculate_status_service import calculate_status


def create_reservation_service(data: Dict, user_authenticated: bool) -> None:

    client_name: str = data.get("client_name")
    people_quantity: int = data.get("people_quantity")
    table_number: int = data.get("table_number")
    booking_date: date = data.get("booking_date")
    initial_time: time = data.get("initial_time")
    final_time: time = data.get("final_time")

    table = __get_table_or_fail(table_number)

    __check_reservation_exists(user_authenticated)
    __check_reservation_time_conflict(
        table_number, booking_date, initial_time, final_time
    )
    __check_table_capacity(table, people_quantity)

    reservation = Reservation(
        client_name=client_name,
        people_quantity=people_quantity,
        table_number=table.table_number,
        booking_date=booking_date,
        initial_time=initial_time,
        final_time=final_time,
    )

    table.status = calculate_status(booking_date, initial_time)

    db.session.add(reservation)
    db.session.commit()


def __get_table_or_fail(table_number: int) -> Table:
    table = Table.query.filter_by(table_number=table_number).first()
    if table is None:
        raise ValueError("Mesa não encontrada")
    return table


def __check_table_capacity(table: Table, people_quantity: int) -> None:
    if people_quantity > table.people_capacity:
        raise ConflictError(
            message="Quantidade de pessoas acima da capacidade da mesa!"
        )


def __get_all_the_reservations() -> List[Reservation]:
    all_the_reservations = Reservation.query.all()
    return all_the_reservations


def __check_reservation_exists(user_authenticated: bool) -> None:
    all_the_reservations = __get_all_the_reservations()
    if all_the_reservations and not user_authenticated:
        raise UnauthorizedError(message="Usuário precisa estar autenticado")


def __get_reservations_by_table_and_date(
    table_number: int, booking_date: date
) -> List[Reservation]:
    reservations_by_table_and_date = Reservation.query.filter_by(
        table_number=table_number, booking_date=booking_date
    ).all()
    return reservations_by_table_and_date


def __check_reservation_time_conflict(
    table_number: int, booking_date: date, initial_time: time, final_time: time
) -> None:
    reservations_by_table_and_date = __get_reservations_by_table_and_date(
        table_number, booking_date
    )

    for r in reservations_by_table_and_date:

        if not (final_time <= r.initial_time or initial_time >= r.final_time):
            raise ConflictError(message="Já existe reserva agendada para esse horario!")
