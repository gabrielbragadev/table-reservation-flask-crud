from app.application.commands.table.table_ownership_command import TableOwnershipCommand
from app.domain.exceptions import ConflictError
from app.domain.repositories.table_repository import TableRepository


class TableRules:

    @staticmethod
    def __get_all_tables(table_repository: TableRepository) -> None:
        return table_repository.find_all()

    @staticmethod
    def __is_table_number_taken(
        table_repository: TableRepository, command: TableOwnershipCommand
    ) -> bool:
        all_tables = TableRules.__get_all_tables(table_repository)
        for t in all_tables:
            if command.data.table_number == t.table_number:
                return True
        return False

    @staticmethod
    def __ensure_table_number() -> None:
        raise ConflictError(message="Já existe uma mesa cadastrada com esse número.")

    @staticmethod
    def validate_table_number(
        table_repository: TableRepository, command: TableOwnershipCommand
    ) -> None:
        if TableRules.__is_table_number_taken(table_repository, command):
            TableRules.__ensure_table_number()
