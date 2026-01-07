from app.exceptions import NotFoundError
from app.repositories.reservation_repository import ReservationRepository


def get_reservation_service(reservation_id: int) -> dict:

    reservation_repository = ReservationRepository()
    reservation = reservation_repository.find_by_id(reservation_id)
    if not reservation:
        raise NotFoundError(message="Reserva não encontrada")

    return reservation.to_dict()
