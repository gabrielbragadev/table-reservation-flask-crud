from dataclasses import dataclass
from datetime import date, time
from typing import Dict, Optional


@dataclass(frozen=True)
class ReadReservationDTO:
    reservation_id: int
    client_name: Optional[str] = None
    people_quantity: Optional[int] = None
    table_number: Optional[int] = None
    booking_date: Optional[date] = None
    initial_time: Optional[time] = None
    final_time: Optional[time] = None
    status: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "reservation_id": self.reservation_id,
            "client_name": self.client_name,
            "people_quantity": self.people_quantity,
            "table_number": self.table_number,
            "booking_date": self.booking_date,
            "initial_time": self.initial_time,
            "final_time": self.final_time,
            "status": self.status,
        }
