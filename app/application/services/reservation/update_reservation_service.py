from typing import Dict
from sqlalchemy.orm import Session

from app.domains.exceptions import NotFoundError
from app.domains.entities.reservation import Reservation
from app.domains.entities.table import Table
from app.domains.repositories.table_repository import TableRepository
from app.domains.repositories.reservation_repository import ReservationRepository
from app.application.services.global_services.exists_time_conflict import ReservationTimeConflict
from app.application.services.global_services.check_table_capacity import check_table_capacity


class UpdateReservationsService:

    def __init__(self, data: Dict, reservation_id: int, session: Session) -> None:
        self.__session = session
        self.__reservation_id = reservation_id
        self.__table_number = data.get("table_number")
        self.__people_quantity = data.get("people_quantity")
        self.__booking_date = data.get("booking_date")
        self.__initial_time = data.get("initial_time")
        self.__final_time = data.get("final_time")
        self.__reservation_repository = ReservationRepository(self.__session)
        self.__table_repository = TableRepository(self.__session)
        self.__reservation_time_conflict = ReservationTimeConflict(self.__session)

    def to_execute(self) -> Reservation:

        reservation_to_update = self.__reservation_repository.find_by_id(
            self.__reservation_id
        )
        self.__check_reservation_exists(reservation_to_update)
        self.__validate_table_number_in_request(reservation_to_update)
        self.__validate_booking_date_in_request(reservation_to_update)

        table_reservation = self.__check_table_exists()

        check_table_capacity(table_reservation, self.__people_quantity)
        self.__reservation_time_conflict.check(
            self.__table_number,
            self.__booking_date,
            self.__initial_time,
            self.__final_time,
            reservation_to_update.id,
        )

        reservation_to_update.table_number = self.__table_number
        reservation_to_update.booking_date = self.__booking_date

        if self.__people_quantity is not None:
            reservation_to_update.people_quantity = self.__people_quantity
        if self.__initial_time is not None:
            reservation_to_update.initial_time = self.__initial_time
        if self.__final_time is not None:
            reservation_to_update.final_time = self.__final_time

        table_reservation.status

        self.__reservation_repository.updated()

        return reservation_to_update

    def __validate_table_number_in_request(
        self, reservation_to_update: Reservation
    ) -> None:
        if self.__table_number is None:
            self.__table_number = reservation_to_update.table_number

    def __validate_booking_date_in_request(self, reservation_to_update: Reservation):
        if self.__booking_date is None:
            self.__booking_date = reservation_to_update.booking_date

    def __check_table_exists(self) -> Table:
        table_reservation = self.__table_repository.find_by_table_number(
            self.__table_number
        )
        if not table_reservation:
            raise NotFoundError(message="Mesa não encontrada")
        return table_reservation

    def __check_reservation_exists(self, reservation_to_update: Reservation) -> None:
        if not reservation_to_update:
            raise NotFoundError(message="Reserva não encontrada")
