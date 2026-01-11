from typing import Dict
from sqlalchemy.orm import Session

from app.models.reservation import Reservation
from app.models.table import Table
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.table_repository import TableRepository
from app.services.global_services.exists_time_conflict import ReservationTimeConflict
from app.services.global_services.check_table_capacity import check_table_capacity


class CreateReservationService:
    def __init__(self, data: Dict, session: Session):
        self.session = session
        self.client_name = data["client_name"]
        self.people_quantity = data["people_quantity"]
        self.table_number = data["table_number"]
        self.booking_date = data["booking_date"]
        self.initial_time = data["initial_time"]
        self.final_time = data["final_time"]
        self.reservation_repository = ReservationRepository(session)
        self.table_repository = TableRepository(session)
        self.reservation_time_conflict = ReservationTimeConflict(session)

    def create_reservation(self) -> Reservation:

        table = self.__check_table_exists()

        self.reservation_time_conflict.check(
            self.table_number, self.booking_date, self.initial_time, self.final_time
        )
        check_table_capacity(table, self.people_quantity)

        reservation = Reservation(
            client_name=self.client_name,
            people_quantity=self.people_quantity,
            table_number=table.table_number,
            booking_date=self.booking_date,
            initial_time=self.initial_time,
            final_time=self.final_time,
            status="active",
        )

        self.reservation_repository.create(reservation)

        return reservation

    def __check_table_exists(self) -> Table:
        table = self.table_repository.find_by_table_number(self.table_number)
        if table is None:
            raise ValueError("Mesa não encontrada")
        return table
