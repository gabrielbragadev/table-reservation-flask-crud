from datetime import date
from typing import List
from app.models.reservation import Reservation
from app.extensions import db


class ReservationRepository:

    def find_all(self) -> List[Reservation]:
        all_the_reservations = Reservation.query.all()
        return all_the_reservations

    def find_by_id(self, reservation_id: int) -> Reservation:
        reservation = Reservation.query.filter_by(id=reservation_id).first()
        return reservation

    def find_by_table_and_date(
        self, table_number: int, booking_date: date
    ) -> List[Reservation]:
        reservations_by_table_and_date = Reservation.query.filter_by(
            table_number=table_number, booking_date=booking_date
        ).all()
        return reservations_by_table_and_date

    def create(self, reservation: Reservation) -> None:
        db.session.add(reservation)
        db.session.commit()

    def delete(self, reservation: Reservation) -> None:
        db.session.delete(reservation)
        db.session.commit()

    def updated(self) -> None:
        db.session.commit()
