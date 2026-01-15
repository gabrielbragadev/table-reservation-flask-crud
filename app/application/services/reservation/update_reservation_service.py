from app.application.commands.reservation.update_reservation_command import (
    UpdateReservationCommand,
)
from app.domain.entities.reservation import Reservation
from app.domain.repositories.reservation_repository import ReservationRepository
from app.domain.services.reservation.reservation_conflict_checker import (
    ReservationConflictChecker,
)
from app.domain.services.reservation.reservation_table_provider import (
    ReservationTableProvider,
)
from app.domain.uow.unit_of_work import UnitOfWork
from app.domain.rules.reservation_rules import ReservationRules


class UpdateReservationsService:

    def __init__(
        self,
        reservation_repository: ReservationRepository,
        conflict_checker: ReservationConflictChecker,
        reservation_table_provider: ReservationTableProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        self.__reservation_repository = reservation_repository
        self.__reservation_to_update = None
        self.__conflict_checker = conflict_checker
        self.__table_provider = reservation_table_provider
        self.__uow = unit_of_work
        self.__table_number = None
        self.__booking_date = None
        self.__table_reservation = None
        self.__command = None

    def to_execute(self, command: UpdateReservationCommand) -> Reservation:

        self.__command = command
        self.__table_number = command.dto.table_number
        self.__booking_date = command.dto.booking_date

        self.__can_update_other_reservation()

        self.__get_reservation_to_update()
        ReservationRules.check_reservation_exists(self.__reservation_to_update)

        self.__get_effective_table_number()
        self.__get_effective_booking_date()
        self.__get_table_reservation()

        self.__check_table_capacity()
        self.__validate_time_conflict()

        self.__reservation_to_update.table_number = self.__table_number
        self.__reservation_to_update.booking_date = self.__booking_date

        if self.__command.dto.people_quantity is not None:
            self.__reservation_to_update.people_quantity = (
                self.__command.dto.people_quantity
            )
        if self.__command.dto.initial_time is not None:
            self.__reservation_to_update.initial_time = self.__command.dto.initial_time
        if self.__command.dto.final_time is not None:
            self.__reservation_to_update.final_time = self.__command.dto.final_time

        self.__uow.commit()

        return self.__reservation_to_update

    def __can_update_other_reservation(self):
        ReservationRules.check_permission_for_modification(
            self.__command.requester_role,
            self.__command.reservation_id,
            self.__command.requester_user_id,
        )

    def __get_reservation_to_update(self) -> None:
        self.__reservation_to_update = self.__reservation_repository.find_by_id(
            self.__command.reservation_id
        )

    def __get_effective_table_number(self) -> None:
        self.__table_number = ReservationRules.load_table_number_to_updt(
            self.__table_number, self.__reservation_to_update
        )

    def __get_effective_booking_date(self) -> None:
        self.__booking_date = ReservationRules.load_booking_date_to_updt(
            self.__booking_date, self.__reservation_to_update
        )

    def __get_table_reservation(self) -> None:
        self.__table_reservation = self.__table_provider.get_table_from_reservation(
            self.__table_number
        )

    def __check_table_capacity(self) -> None:
        ReservationRules.check_table_capacity(
            self.__table_reservation, self.__command.dto.people_quantity
        )

    def __has_conflict(self) -> bool:
        has_conflict = self.__conflict_checker.exists(
            self.__table_number,
            self.__booking_date,
            self.__command.dto.initial_time,
            self.__command.dto.final_time,
            self.__command.reservation_id,
        )
        return has_conflict

    def __validate_time_conflict(self) -> None:
        ReservationRules.validate_time_conflict(self.__has_conflict())
