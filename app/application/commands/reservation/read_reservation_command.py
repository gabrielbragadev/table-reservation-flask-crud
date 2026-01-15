from dataclasses import dataclass
from datetime import date
from app.application.dtos.reservation.read_reservation_dto import ReadReservationDTO


@dataclass(frozen=True)
class ReadReservationCommand:
    requester_role: str
    requester_user_id: int
    dto: ReadReservationDTO

    date_from: date | None = None
    date_to: date | None = None
