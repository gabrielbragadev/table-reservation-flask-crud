from app.exceptions import ConflictError
from app.models.table import Table



def check_table_capacity(table: Table, people_quantity: int | None) -> None:

    if people_quantity is None:
        return

    if people_quantity > table.people_capacity:
        raise ConflictError(
            message="Quantidade de pessoas acima da capacidade da mesa!"
        )
