from dataclasses import dataclass
from datetime import date
from app.application.dtos.user.create_user_dto import CreateUserDTO


@dataclass(frozen=True)
class CreateUserCommand:

    data: CreateUserDTO

    requester_role: None = None
    requester_user_id: None = None
    date_from: date | None = None
    date_to: date | None = None
