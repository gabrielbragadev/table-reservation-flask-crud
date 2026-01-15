from sqlalchemy.orm import Session
from app.domain.repositories.reservation_repository import ReservationRepository
from datetime import date
from typing import List
from app.domain.entities.reservation import Reservation


class ReservationRepository(ReservationRepository):

    def __init__(self, session):
        self.session: Session = session

    def save(self, reservation: Reservation):
        self.session.add(reservation)

    def find_by_id(self, reservation_id: int) -> Reservation:
        reservation = (
            self.session.query(Reservation).filter_by(id=reservation_id).first()
        )
        return reservation

    def find_by_table_and_date(
        self, table_number: int, booking_date: date
    ) -> List[Reservation]:

        reservations_by_table_and_date = (
            self.session.query(Reservation)
            .filter_by(table_number=table_number, booking_date=booking_date)
            .all()
        )

        return reservations_by_table_and_date

    def find_all(self) -> List[Reservation]:
        all_the_reservations = self.session.query(Reservation).all()
        return all_the_reservations

    def delete(self, reservation: Reservation) -> None:
        self.session.delete(reservation)
