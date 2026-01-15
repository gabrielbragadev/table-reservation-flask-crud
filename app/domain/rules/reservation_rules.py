from datetime import date
from app.domain.entities.reservation import Reservation
from app.domain.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.domain.entities.table import Table


class ReservationRules:

    @staticmethod
    def check_table_capacity(table: Table, people_quantity: int | None) -> None:
        if people_quantity is None:
            return

        if people_quantity > table.people_capacity:

            raise ConflictError(
                message="Quantidade de pessoas acima da capacidade da mesa!"
            )

    @staticmethod
    def validate_time_conflict(has_conflict: bool) -> None:
        if has_conflict:
            raise ConflictError(message="Já existe reserva nesse horário")

    @staticmethod
    def check_permission_for_modification(
        requester_role: str, reservation_id: int, requester_user_id: int
    ) -> None:
        if requester_role != "admin" and reservation_id != requester_user_id:
            raise ForbiddenError(
                message="Você não tem permissão para acessar esta reserva"
            )

    @staticmethod
    def check_permission_to_see_all(requester_role: str) -> None:
        if requester_role != "admin":
            raise ForbiddenError(
                message="Você não tem permissão para acessar esse recurso"
            )

    @staticmethod
    def check_reservation_exists(reservation: Reservation) -> None:
        if not reservation:
            raise NotFoundError(message="Reserva não encontrada")

    @staticmethod
    def load_table_number_to_updt(table_number: int, reservation: Reservation) -> int:
        if table_number is None:
            return reservation.table_number
        return table_number

    @staticmethod
    def load_booking_date_to_updt(booking_date: date, reservation: Reservation) -> date:
        if booking_date is None:
            return reservation.booking_date
        return booking_date
