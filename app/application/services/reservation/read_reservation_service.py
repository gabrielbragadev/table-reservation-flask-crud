from typing import Dict
from sqlalchemy.orm import Session
from app.domains.exceptions import NotFoundError
from app.domains.entities.reservation import Reservation
from app.domains.repositories.reservation_repository import ReservationRepository


class GetReservationService:
    def __init__(self, reservation_id: int, session: Session) -> None:
        self.__session = session
        self.__reservation_repository = ReservationRepository(self.__session)
        self.__reservation_id = reservation_id

    def to_execute(self) -> Dict[Reservation]:

        reservation = self.__reservation_repository.find_by_id(self.__reservation_id)
        if not reservation:
            raise NotFoundError(message="Reserva não encontrada")

        return reservation.to_dict()
