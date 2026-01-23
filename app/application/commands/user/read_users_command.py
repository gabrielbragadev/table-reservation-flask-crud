from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ReadUsersCommand:
    requester_role: str
    requester_user_id: Optional[int]
    date_from: Optional[str] = None
    date_to: Optional[str] = None
