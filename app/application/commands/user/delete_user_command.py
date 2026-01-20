from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteUserCommand:
    user_id: int
    requester_user_id: int
    requester_role: str
    otp_code: str | None = None
