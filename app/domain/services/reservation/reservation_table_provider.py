from app.application.commands.reservation.create_reservation_command import (
    CreateReservationCommand,
)

from app.domain.entities.table import Table
from app.domain.exceptions import NotFoundError
from app.domain.repositories.table_repository import TableRepository


class ReservationTableProvider:

    def __init__(
        self,
        table_repository: TableRepository,
    ):
        self.__table_repository = table_repository

    def get_table_from_reservation(self, table_number: int) -> Table:
        table = self.__table_repository.find_by_table_number(table_number)
        if table is None:
            raise NotFoundError(message="Mesa não encontrada")
        return table
