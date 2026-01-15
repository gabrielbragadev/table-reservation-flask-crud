from dataclasses import dataclass
from app.application.dtos.reservation.update_reservation_dto import (
    UpdateReservationDTO,
)


@dataclass(frozen=True)
class UpdateReservationCommand:
    reservation_id: int
    dto: UpdateReservationDTO
    requester_user_id: int
    requester_role: str
