from dataclasses import dataclass
from datetime import date, time
from typing import Dict, Optional


@dataclass(frozen=True)
class UpdateReservationDTO:
    people_quantity: Optional[int] = None
    table_number: Optional[int] = None
    booking_date: Optional[date] = None
    initial_time: Optional[time] = None
    final_time: Optional[time] = None

    def to_dict(self) -> Dict:
        return {
            k: v
            for k, v in {
                "people_quantity": self.people_quantity,
                "table_number": self.table_number,
                "booking_date": self.booking_date,
                "initial_time": self.initial_time,
                "final_time": self.final_time,
            }.items()
            if v is not None
        }
