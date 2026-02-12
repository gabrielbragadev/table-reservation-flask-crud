from dataclasses import dataclass
from datetime import date, time
from typing import Optional


@dataclass(frozen=True)
class CreateReservationDTO:
    client_name: str
    people_quantity : int
    table_number : int
    booking_date : date
    initial_time : time
    final_time : time
    
    
