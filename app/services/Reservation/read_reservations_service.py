from typing import List

from app.exceptions import NotFoundError
from app.repositories.reservation_repository import ReservationRepository


def get_reservations_service() -> List[dict]:
    reservation_repository = ReservationRepository()
    reservations = reservation_repository.find_all()

    if not reservations:
        raise NotFoundError(message="Nenhum registro encontrado")
    response = [r.to_dict() for r in reservations]
    return response
