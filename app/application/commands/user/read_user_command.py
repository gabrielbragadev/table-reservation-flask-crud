from dataclasses import dataclass
from datetime import date
from app.application.dtos.user.read_user_dto import ReadUserDTO


@dataclass(frozen=True)
class ReadUserCommand:
    user_id: int
    requester_role: str
    requester_user_id: int
    dto: ReadUserDTO

    date_from: date | None = None
    date_to: date | None = None
