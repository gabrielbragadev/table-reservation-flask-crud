from datetime import date, time
from app.exceptions import ConflictError
from app.repositories.reservation_repository import ReservationRepository


def check_reservation_time_conflict(
    table_number: int,
    booking_date: date,
    initial_time: time,
    final_time: time,
    ignore_reservation_id: int | None = None,
) -> None:

    reservation_repository = ReservationRepository()
    reservations_by_table_and_date = reservation_repository.find_by_table_and_date(
        table_number, booking_date
    )

    for r in reservations_by_table_and_date:
        if ignore_reservation_id and r.id == ignore_reservation_id:
            continue

        if not (final_time <= r.initial_time or initial_time >= r.final_time):
            raise ConflictError(message="Já existe reserva agendada para esse horario!")
