from dataclasses import dataclass
from datetime import date
from app.application.dtos.table.table_ownership_dto import TableOwnershipDTO


@dataclass(frozen=True)
class TableOwnershipCommand:

    data: TableOwnershipDTO

    requester_role: None = None
    requester_user_id: None = None
    date_from: date | None = None
    date_to: date | None = None
