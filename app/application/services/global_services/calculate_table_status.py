from datetime import datetime, date, time


from datetime import datetime, date, time

AVAILABLE = "available"
OCCUPIED = "occupied"


def calculate_table_status(
    booking_date: date, reservations: list[tuple[time, time]]
) -> str:

    now = datetime.now()

    if now.date() != booking_date:
        return AVAILABLE

    now_time = now.time()

    for initial_time, final_time in reservations:
        if initial_time <= now_time <= final_time:
            return OCCUPIED

    return "available"
