from dataclasses import dataclass


@dataclass(frozen=True)
class CancelReservationCommand:
    reservation_id: int
    requester_user_id: int
    requester_role: str
