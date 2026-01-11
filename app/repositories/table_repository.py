from app.models.table import Table
from sqlalchemy.orm import Session


class TableRepository:

    def __init__(self, session):
        self.session: Session = session

    def find_by_table_number(self, table_number):
        return self.session.query(Table).filter_by(table_number=table_number).first()
