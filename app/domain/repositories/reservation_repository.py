from abc import ABC, abstractmethod
from datetime import date
from typing import List
from app.domain.entities.reservation import Reservation


class ReservationRepository(ABC):

    @abstractmethod
    def save(self, reservation: Reservation):
        pass

    @abstractmethod
    def find_by_id(self, reservation_id: int) -> Reservation:
        pass

    @abstractmethod
    def find_by_table_and_date(
        self, table_number: int, booking_date: date
    ) -> List[Reservation]:
        pass

    @abstractmethod
    def find_all(self) -> List[Reservation]:
        pass

    @abstractmethod
    def delete(self, reservation: Reservation) -> None:
        pass
