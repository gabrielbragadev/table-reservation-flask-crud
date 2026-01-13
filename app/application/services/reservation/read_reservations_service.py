from typing import Dict, List
from sqlalchemy.orm import Session

from app.domains.exceptions import NotFoundError
from app.domains.repositories.reservation_repository import ReservationRepository


class GetReservationsService:

    def __init__(self, session: Session) -> None:
        self.__session = session
        self.__reservation_repository = ReservationRepository(self.__session)

    def to_execute(self) -> List[Dict]:

        reservations = self.__reservation_repository.find_all()

        if not reservations:
            raise NotFoundError(message="Nenhum registro encontrado")
        response = [r.to_dict() for r in reservations]
        return response
