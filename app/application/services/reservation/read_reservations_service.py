from typing import Dict, List

from app.application.commands.reservation.read_reservations_command import (
    ReadReservationsCommand,
)
from app.application.dtos.reservation.read_reservation_dto import ReadReservationDTO
from app.application.dtos.reservation.read_reservations_dto import ReadReservationsDTO
from app.domain.exceptions import NotFoundError
from app.domain.repositories.reservation_repository import ReservationRepository
from app.domain.rules.reservation_rules import ReservationRules


class GetReservationsService:

    def __init__(self, reservation_repository: ReservationRepository) -> None:
        self.__reservation_repository = reservation_repository

    def to_execute(self, command: ReadReservationsCommand) -> List[Dict]:

        ReservationRules.check_permission_to_see_all(command.requester_role)

        reservations = self.__reservation_repository.find_all()
        if not reservations:
            raise NotFoundError(message="Nenhum registro encontrado")

        dtos = [
            ReadReservationDTO(
                r.reservation_id,
                r.client_name,
                r.people_quantiry,
                r.table_number,
                r.booking_date,
                r.initial_time,
                r.final_time,
                r.status,
            )
            for r in reservations
        ]

        return ReadReservationsDTO(reservations=dtos)
