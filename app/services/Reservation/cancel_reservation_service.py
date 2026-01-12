from sqlalchemy.orm import Session
from app.exceptions import NotFoundError
from app.models.reservation import Reservation
from app.repositories.reservation_repository import ReservationRepository


class CancelReservationService:
    def __init__(self, reservation_id: int, session: Session) -> None:
        self.__reservation_id = reservation_id
        self.__session = session
        self.__reservation_repository = ReservationRepository(self.__session)

    def to_execute(self) -> Reservation:

        reservation = self.__check_reservation_exists()

        reservation.status = "cancelled"

        self.__reservation_repository.create(reservation)

        return reservation

    def __check_reservation_exists(self) -> Reservation:
        reservation = self.__reservation_repository.find_by_id(self.__reservation_id)

        if reservation is None:
            raise NotFoundError("Reserva não encontrada")

        return reservation
