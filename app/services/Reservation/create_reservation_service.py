from typing import Dict
from sqlalchemy.orm import Session

from app.models.reservation import Reservation
from app.models.table import Table
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.table_repository import TableRepository
from app.services.global_services.exists_time_conflict import ReservationTimeConflict
from app.services.global_services.check_table_capacity import check_table_capacity


class CreateReservationService:
    def __init__(self, data: Dict, session: Session) -> None:
        self.__session = session
        self.__client_name = data["client_name"]
        self.__people_quantity = data["people_quantity"]
        self.__table_number = data["table_number"]
        self.__booking_date = data["booking_date"]
        self.__initial_time = data["initial_time"]
        self.__final_time = data["final_time"]
        self.__reservation_repository = ReservationRepository(self.__session)
        self.__table_repository = TableRepository(self.__session)
        self.__reservation_time_conflict = ReservationTimeConflict(self.__session)

    def to_execute(self) -> Reservation:

        table = self.__check_table_exists()

        self.__reservation_time_conflict.check(
            self.__table_number, self.__booking_date, self.__initial_time, self.__final_time
        )
        check_table_capacity(table, self.__people_quantity)

        reservation = Reservation(
            client_name=self.__client_name,
            people_quantity=self.__people_quantity,
            table_number=table.table_number,
            booking_date=self.__booking_date,
            initial_time=self.__initial_time,
            final_time=self.__final_time,
            status="active",
        )

        self.__reservation_repository.create(reservation)

        return reservation

    def __check_table_exists(self) -> Table:
        table = self.__table_repository.find_by_table_number(self.__table_number)
        if table is None:
            raise ValueError("Mesa não encontrada")
        return table
