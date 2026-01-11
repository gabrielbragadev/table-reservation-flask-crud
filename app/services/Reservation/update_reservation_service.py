from datetime import date, time
from typing import Dict

from app.exceptions import ConflictError, NotFoundError
from app.models.reservation import Reservation
from app.models.table import Table
from app.extensions import db
from app.repositories.table_repository import TableRepository
from app.repositories.reservation_repository import ReservationRepository
from app.services.global_services.exists_time_conflict import (
    check_reservation_time_conflict,
)
from app.services.global_services.check_table_capacity import check_table_capacity


def update_reservation_service(data: Dict, reservation_id: int) -> Reservation:

    reservation_to_update = __get_reservation_to_update(reservation_id)
    __check_reservation_exists(reservation_to_update)

    table_number = (
        data.get("table_number")
        if data.get("table_number") is not None
        else reservation_to_update.table_number
    )

    people_quantity = data.get("people_quantity")

    booking_date = (
        data.get("booking_date")
        if data.get("booking_date") is not None
        else reservation_to_update.booking_date
    )

    initial_time = data.get("initial_time")

    final_time = data.get("final_time")

    reservation_repository = __get_reservation_repository()

    table_reservation = __check_table_exists(table_number)

    check_table_capacity(table_reservation, people_quantity)

    check_reservation_time_conflict(
        table_number, booking_date, initial_time, final_time, reservation_to_update.id
    )

    if table_number is not None:
        reservation_to_update.table_number = table_reservation.table_number
    if people_quantity is not None:
        reservation_to_update.people_quantity = people_quantity
    if booking_date is not None:
        reservation_to_update.booking_date = booking_date
    if initial_time is not None:
        reservation_to_update.initial_time = initial_time
    if final_time is not None:
        reservation_to_update.final_time = final_time

    table_reservation.status

    reservation_repository.updated()

    return reservation_to_update


def __get_reservation_repository() -> ReservationRepository:
    reservation_repository = ReservationRepository()
    return reservation_repository


def __get_reservation_to_update(reservation_id: int) -> Reservation:
    reservation_repository = __get_reservation_repository()
    reservation_to_update = reservation_repository.find_by_id(reservation_id)
    return reservation_to_update


def __check_table_exists(table_number: int) -> Table:
    table_repository = TableRepository()
    table_reservation = table_repository.find_by_table_number(table_number)
    if not table_reservation:
        raise NotFoundError(message="Mesa não encontrada")
    return table_reservation


def __check_reservation_exists(reservation_to_update: Reservation) -> None:
    if not reservation_to_update:
        raise NotFoundError(message="Reserva não encontrada")
