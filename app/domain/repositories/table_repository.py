from abc import ABC, abstractmethod
from app.domain.entities.table import Table


class TableRepository(ABC):

    @abstractmethod
    def find_by_table_number(self, table_number) -> Table:
        pass
