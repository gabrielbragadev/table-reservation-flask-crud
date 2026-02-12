from app.application.commands.reservation.create_reservation_command import (
    CreateReservationCommand,
)
from app.domain.entities.reservation import Reservation
from app.domain.repositories.reservation_repository import ReservationRepository
from app.domain.rules.reservation_rules import ReservationRules
from app.domain.services.reservation.reservation_conflict_checker import (
    ReservationConflictChecker,
)
from app.domain.services.reservation.reservation_table_provider import (
    ReservationTableProvider,
)
from app.domain.uow.unit_of_work import UnitOfWork


class CreateReservationService:
    def __init__(
        self,
        reservation_repository: ReservationRepository,
        conflict_checker: ReservationConflictChecker,
        reservation_table_provider: ReservationTableProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        self.__reservation_repository = reservation_repository
        self.__conflict_checker = conflict_checker
        self.__table_provider = reservation_table_provider
        self.__uow = unit_of_work
        self.__table = None
        self.__command = None

    def to_execute(self, command: CreateReservationCommand) -> Reservation:

        self.__command = command
        self.__get_table_reservation()

        self.__check_table_capacity()
        self.__validate_time_conflict()

        reservation = Reservation(
            client_name=self.__command.data.client_name,
            people_quantity=self.__command.data.people_quantity,
            table_number=self.__command.data.table_number,
            booking_date=self.__command.data.booking_date,
            initial_time=self.__command.data.initial_time,
            final_time=self.__command.data.final_time,
            status="active",
        )

        self.__reservation_repository.save(reservation)
        self.__uow.commit()

        return reservation

    def __get_table_reservation(self) -> None:
        self.__table = self.__table_provider.get_table_from_reservation(
            self.__command.data.table_number
        )

    def __check_table_capacity(self) -> None:
        ReservationRules.check_table_capacity(
            self.__table, self.__command.data.people_quantity
        )

    def __has_conflict(self) -> bool:
        has_conflict = self.__conflict_checker.exists(
            self.__command.data.table_number,
            self.__command.data.booking_date,
            self.__command.data.initial_time,
            self.__command.data.final_time,
        )
        return has_conflict

    def __validate_time_conflict(self) -> None:
        ReservationRules.validate_time_conflict(self.__has_conflict())
