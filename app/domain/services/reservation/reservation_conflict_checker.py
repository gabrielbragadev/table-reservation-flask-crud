from datetime import date, time
from app.domain.repositories.reservation_repository import ReservationRepository


class ReservationConflictChecker:
    def __init__(self, reservation_repository: ReservationRepository) -> None:
        self.__reservation_repository = reservation_repository

    def exists(
        self,
        table_number: int,
        booking_date: date,
        initial_time: time,
        final_time: time,
        ignore_reservation_id=None,
    ) -> bool:

        reservations_by_table_and_date = (
            self.__reservation_repository.find_by_table_and_date(
                table_number, booking_date
            )
        )

        for r in reservations_by_table_and_date:
            if ignore_reservation_id and r.id == ignore_reservation_id:
                continue

            if not (final_time <= r.initial_time or initial_time >= r.final_time):
                return True

        return False
