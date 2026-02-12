from dataclasses import dataclass
from app.application.dtos.user.update_user_dto import UpdateUserDTO


@dataclass(frozen=True)
class UpdateUserCommand:
    user_id: int
    dto: UpdateUserDTO
    requester_user_id: int
    requester_role: str
