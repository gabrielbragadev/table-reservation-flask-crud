from datetime import date
from typing import Protocol


class UserOwnershipCommand(Protocol):
    user_id: int
    requester_role: str
    requester_user_id: int

    date_from: date | None = None
    date_to: date | None = None
