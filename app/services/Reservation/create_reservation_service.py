from datetime import date, time
from typing import Dict

from app.models.reservation import Reservation
from app.models.table import Table
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.table_repository import TableRepository
from app.services.global_services.exists_time_conflict import (
    check_reservation_time_conflict,
)
from app.services.global_services.check_table_capacity import check_table_capacity


def create_reservation_service(data: Dict) -> Reservation:

    client_name: str = data["client_name"]
    people_quantity: int = data["people_quantity"]
    table_number: int = data["table_number"]
    booking_date: date = data["booking_date"]
    initial_time: time = data["initial_time"]
    final_time: time = data["final_time"]

    table = _check_table_exists(table_number)

    check_reservation_time_conflict(
        table_number, booking_date, initial_time, final_time
    )
    check_table_capacity(table, people_quantity)

    reservation = Reservation(
        client_name=client_name,
        people_quantity=people_quantity,
        table_number=table.table_number,
        booking_date=booking_date,
        initial_time=initial_time,
        final_time=final_time,
        status="active",
    )

    reservation_repository = ReservationRepository()
    reservation_repository.create(reservation)

    return reservation


def _check_table_exists(table_number: int) -> Table:
    table_repository = TableRepository()
    table = table_repository.find_by_table_number(table_number)
    if table is None:
        raise ValueError("Mesa não encontrada")
    return table
