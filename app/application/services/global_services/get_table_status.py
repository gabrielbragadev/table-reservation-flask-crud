from datetime import date

from app.domain.entities.table import Table
from app.application.services.global_services.calculate_table_status import calculate_table_status


def get_table_status(table: Table) -> str:
    today = date.today()

    today_reservations = [
        (r.initial_time, r.final_time)
        for r in table.reservations
        if r.booking_date == today and r.status == "active"
    ]

    return calculate_table_status(today, today_reservations)
