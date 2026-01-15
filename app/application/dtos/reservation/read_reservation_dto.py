from dataclasses import dataclass
from datetime import date, time
from typing import Dict, Optional


@dataclass(frozen=True)
class ReadReservationDTO:
    reservation_id: int
    client_name: str
    people_quantity: int
    table_number: int
    booking_date: date
    initial_time: time
    final_time: time
    status: str

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
