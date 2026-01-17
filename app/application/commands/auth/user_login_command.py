from dataclasses import dataclass
from app.application.dtos.auth.user_login_dto import UserLoginDTO


@dataclass(frozen=True)
class UserLoginCommand:
    dto: UserLoginDTO
