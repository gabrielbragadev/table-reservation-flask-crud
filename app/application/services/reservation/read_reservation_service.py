from typing import Any, Dict
from app.application.commands.reservation.read_reservation_command import (
    ReadReservationCommand,
)
from app.domain.exceptions import NotFoundError
from app.domain.repositories.reservation_repository import ReservationRepository
from app.domain.rules.reservation_rules import ReservationRules


class GetReservationService:
    def __init__(self, reservation_repository: ReservationRepository) -> None:
        self.__reservation_repository = reservation_repository
        self.__command = None
        self.__reservation_to_read = None

    def to_execute(self, command: ReadReservationCommand) -> Dict[str, Any]:

        self.__command = command

        self.__check_permission_for_modifications()
        self.__get_reservation_to_read()
        self.__check_reservation_exists()

        return_dict = self.__fill_return_dict()

        return return_dict

    def __check_permission_for_modifications(self):
        ReservationRules.check_permission_for_modification(
            self.__command.requester_role,
            self.__command.reservation_id,
            self.__command.requester_user_id,
        )

    def __get_reservation_to_read(self) -> None:
        self.__reservation_to_read = self.__reservation_repository.find_by_id(
            self.__command.reservation_id
        )

    def __reservation_does_not_exist(self) -> bool:
        return self.__reservation_to_read is None

    def __check_reservation_exists(self) -> None:
        if self.__reservation_does_not_exist():
            raise NotFoundError(message="Reserva não encontrada")

    def __fill_return_dict(self) -> Dict[str, Any]:
        return {
            "booking_date": self.__reservation_to_read.booking_date,
            "client_name": self.__reservation_to_read.client_name,
            "initial_time": self.__reservation_to_read.initial_time,
            "final_time": self.__reservation_to_read.final_time,
            "people_quantity": self.__reservation_to_read.people_quantity,
            "table_number": self.__reservation_to_read.table_number,
            "status": self.__reservation_to_read.status,
        }
