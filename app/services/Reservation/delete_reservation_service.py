from app.exceptions import NotFoundError
from app.models.reservation import Reservation
from app.repositories.reservation_repository import ReservationRepository


def delete_reservation_service(reservation_id: int) -> None:
    reservation = __check_reservation_exists(reservation_id)
    __change_table_status(reservation_id)

    reservation_repository = ReservationRepository()
    reservation_repository.delete(reservation)


def __check_reservation_exists(reservation_id: int) -> Reservation:

    reservation_repository = ReservationRepository()
    reservation = reservation_repository.find_by_id(reservation_id)
    if reservation is None:
        raise NotFoundError(message="Reserva não encontrada")
    return reservation


def __change_table_status(reservation_id: int) -> None:
    reservation_repository = ReservationRepository()
    reservation = reservation_repository.find_by_id(reservation_id)

    if reservation.table:
        reservation.table.status = "Available"
