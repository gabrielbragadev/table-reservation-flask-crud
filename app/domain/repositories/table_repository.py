from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.table import Table


class TableRepository(ABC):

    @abstractmethod
    def save(self, table: Table) -> None:
        pass

    @abstractmethod
    def find_by_table_number(self, table_number) -> Table:
        pass

    def find_all(self) -> List[Table]:
        pass
