from datetime import datetime, date, time


def calculate_status(booking_date: date, initial_time: time, final_time: time) -> str:

    now = datetime.now()

    if now.date() != booking_date:
        return "Available"

    now_time = now.time()

    if initial_time <= now_time <= final_time:
        return "Occupied"

    return "Available"
