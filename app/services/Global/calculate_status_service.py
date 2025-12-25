from datetime import datetime


def calculate_status(booking_date, initial_time):
    now = datetime.now()
    booking_datetime = datetime.combine(booking_date, initial_time)

    return "Reserved" if now < booking_datetime else "Available"
