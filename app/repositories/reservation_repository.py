from sqlalchemy.orm import Session
from datetime import date
from typing import List
from app.models.reservation import Reservation
from app.extensions import db


class ReservationRepository:

    def __init__(self, session):
        self.session: Session = session

    def save(self, reservation):
        self.session.add(reservation)
        self.session.commit()

    def find_all(self) -> List[Reservation]:
        all_the_reservations = self.session.query(Reservation).all()
        return all_the_reservations

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

    def create(self, reservation: Reservation) -> None:
        self.session.add(reservation)
        self.session.commit()

    def delete(self, reservation: Reservation) -> None:
        self.session.delete(reservation)
        self.session.commit()

    def updated(self) -> None:
        self.session.commit()
