from dataclasses import dataclass
from datetime import date
from app.application.dtos.table.create_table_dto import CreateTableDTO


@dataclass(frozen=True)
class CreateTableCommand:

    data: CreateTableDTO

    requester_role: None = None
    requester_user_id: None = None
    date_from: date | None = None
    date_to: date | None = None
