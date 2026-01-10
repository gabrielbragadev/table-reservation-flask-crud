from app.models.table import Table


class TableRepository:

    def find_by_table_number(self, table_number=int) -> Table:
        table = Table.query.filter_by(table_number=table_number).first()
        return table
    
    
