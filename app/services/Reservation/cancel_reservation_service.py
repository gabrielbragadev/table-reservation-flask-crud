from app.exceptions import NotFoundError
from app.models.reservation import Reservation
from app.repositories.reservation_repository import ReservationRepository


def cancel_reservation_service(reservation_id: int) -> Reservation:
    reservation_repository = ReservationRepository()
    reservation = reservation_repository.find_by_id(reservation_id)

    if reservation is None:
        raise NotFoundError("Reserva não encontrada")

    reservation.status = "cancelled"

    reservation_repository.create(reservation)

    return reservation
