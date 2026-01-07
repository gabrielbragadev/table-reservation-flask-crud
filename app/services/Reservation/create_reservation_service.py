from datetime import date, time
from typing import Dict

from app.exceptions import ConflictError, UnauthorizedError
from app.models.reservation import Reservation
from app.models.table import Table
from app.services.global_services.calculate_status_service import calculate_status
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.table_repository import TableRepository


def create_reservation_service(data: Dict, user_authenticated: bool) -> None:

    client_name: str = data.get("client_name")
    people_quantity: int = data.get("people_quantity")
    table_number: int = data.get("table_number")
    booking_date: date = data.get("booking_date")
    initial_time: time = data.get("initial_time")
    final_time: time = data.get("final_time")

    table = __check_table_exists(table_number)

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

    table.status = calculate_status(booking_date, initial_time, final_time)

    reservation_repository = ReservationRepository()
    reservation_repository.create(reservation)


def __check_table_exists(table_number: int) -> Table:
    table_repository = TableRepository()
    table = table_repository.find_by_table_number(table_number)
    if table is None:
        raise ValueError("Mesa não encontrada")
    return table


def __check_table_capacity(table: Table, people_quantity: int) -> None:
    if people_quantity > table.people_capacity:
        raise ConflictError(
            message="Quantidade de pessoas acima da capacidade da mesa!"
        )


def __check_reservation_time_conflict(
    table_number: int, booking_date: date, initial_time: time, final_time: time
) -> None:
    reservation_repository = ReservationRepository()
    reservations_by_table_and_date = reservation_repository.find_by_table_and_date(
        table_number, booking_date
    )

    for r in reservations_by_table_and_date:

        if not (final_time <= r.initial_time or initial_time >= r.final_time):
            raise ConflictError(message="Já existe reserva agendada para esse horario!")
