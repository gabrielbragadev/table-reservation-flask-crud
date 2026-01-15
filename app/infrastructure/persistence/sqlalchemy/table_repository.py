from sqlalchemy.orm import Session
from app.domain.repositories.table_repository import TableRepository
from app.domain.entities.table import Table


class TableRepository(TableRepository):

    def __init__(self, session):
        self.session: Session = session

    def find_by_table_number(self, table_number) -> Table:
        return self.session.query(Table).filter_by(table_number=table_number).first()
