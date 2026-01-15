from app.application.commands.reservation.read_reservation_command import (
    ReadReservationCommand,
)
from app.domain.exceptions import NotFoundError
from app.domain.entities.reservation import Reservation
from app.domain.repositories.reservation_repository import ReservationRepository
from app.domain.rules.reservation_rules import ReservationRules


class GetReservationService:
    def __init__(self, reservation_repository: ReservationRepository) -> None:
        self.__reservation_repository = reservation_repository

    def to_execute(self, command: ReadReservationCommand) -> Reservation:

        ReservationRules.check_permission_for_modification(
            command.requester_role,
            command.dto.reservation_id,
            command.requester_user_id,
        )

        reservation = self.__reservation_repository.find_by_id(
            command.dto.reservation_id
        )
        if not reservation:
            raise NotFoundError(message="Reserva não encontrada")

        return reservation
