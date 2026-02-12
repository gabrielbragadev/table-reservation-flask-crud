from dataclasses import dataclass
from typing import List, Dict

from app.application.dtos.reservation.read_reservation_dto import ReadReservationDTO


@dataclass(frozen=True)
class ReadReservationsDTO:
    reservations: List[ReadReservationDTO]

    def to_list_of_dicts(self) -> List[Dict]:
        return [r.to_dict() for r in self.reservations]
