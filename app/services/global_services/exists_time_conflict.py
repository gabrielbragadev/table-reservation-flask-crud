from sqlalchemy.orm import Session
from datetime import date, time
from app.exceptions import ConflictError
from app.repositories.reservation_repository import ReservationRepository


class ReservationTimeConflict:
    def __init__(self, session: Session) -> None:
        self.__session = session
        self.__reservation_repository = ReservationRepository(self.__session)

    def check(
        self,
        table_number: int,
        booking_date: date,
        initial_time: time,
        final_time: time,
        ignore_reservation_id=None,
    ) -> None:

        reservations_by_table_and_date = (
            self.__reservation_repository.find_by_table_and_date(
                table_number, booking_date
            )
        )

        for r in reservations_by_table_and_date:
            if ignore_reservation_id and r.id == ignore_reservation_id:
                continue

            if not (final_time <= r.initial_time or initial_time >= r.final_time):
                raise ConflictError(
                    message="Já existe reserva agendada para esse horario!"
                )
