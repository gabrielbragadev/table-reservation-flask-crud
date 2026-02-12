from app.application.commands.table.create_table_command import CreateTableCommand
from app.domain.repositories.table_repository import TableRepository
from app.domain.rules.table_rules import TableRules
from app.domain.rules.user_rules import UserRules
from app.domain.uow.unit_of_work import UnitOfWork
from app.domain.entities.table import Table


class CreateTableService:

    def __init__(
        self, table_repository: TableRepository, unit_of_work: UnitOfWork
    ) -> None:
        self.__table_repository = table_repository
        self.__command = None
        self.__uow = unit_of_work

    def to_execute(self, command: CreateTableCommand) -> Table:
        self.__command = command

        self.__validate_admin_access()
        self.__validate_table_number()

        table = Table(
            table_number=self.__command.data.table_number,
            people_capacity=self.__command.data.people_capacity,
        )
        self.__table_repository.save(table)
        self.__uow.commit()

        return table

    def __validate_admin_access(self) -> None:
        UserRules.validate_user_role_permission(self.__command)

    def __validate_table_number(self) -> None:
        TableRules.validate_table_number(self.__table_repository, self.__command)
