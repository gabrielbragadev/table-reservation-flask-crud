from app.domain.exceptions import NotFoundError
from app.domain.entities.reservation import Reservation
from app.domain.repositories.reservation_repository import ReservationRepository
from app.application.commands.reservation.cancel_reservation_command import (
    CancelReservationCommand,
)
from app.domain.uow.unit_of_work import UnitOfWork
from app.domain.rules.reservation_rules import ReservationRules


class CancelReservationService:
    def __init__(
        self, reservation_repository: ReservationRepository, unit_of_work: UnitOfWork
    ) -> None:
        self.__reservation_repository = reservation_repository
        self.__uow = unit_of_work
        self.__command = None

    def to_execute(self, command: CancelReservationCommand) -> Reservation:
        self.__command = command

        reservation = self.__get_reservation_to_cancel()

        reservation.status = "cancelled"

        self.__reservation_repository.save(reservation)
        self.__uow.commit()
        return reservation

    def __get_reservation_to_cancel(
        self,
    ) -> Reservation:

        ReservationRules.check_permission_for_modification(
            self.__command.requester_role,
            self.__command.reservation_id,
            self.__command.requester_user_id,
        )
        reservation = self.__reservation_repository.find_by_id(
            self.__command.reservation_id
        )

        if reservation is None:
            raise NotFoundError(message="Reserva não encontrada")

        return reservation
