from dataclasses import dataclass
from typing import Optional
from app.application.dtos.reservation.read_reservations_dto import ReadReservationsDTO


@dataclass(frozen=True)
class ReadReservationsCommand:
    requester_role: str
    requester_user_id: Optional[int]
    date_from: Optional[str] = None
    date_to: Optional[str] = None
