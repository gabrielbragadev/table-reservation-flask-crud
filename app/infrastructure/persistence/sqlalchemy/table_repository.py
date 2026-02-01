from typing import List
from sqlalchemy.orm import Session
from app.domain.repositories.table_repository import TableRepository
from app.domain.entities.table import Table


class TableRepository(TableRepository):

    def __init__(self, session):
        self.session: Session = session

    def save(self, table: Table) -> None:
        self.session.add(table)

    def find_by_table_number(self, table_number) -> Table:
        return self.session.query(Table).filter_by(table_number=table_number).first()

    def find_all(self) -> List[Table]:
        return self.session.query(Table).all()
