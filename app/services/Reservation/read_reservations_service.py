from flask import jsonify

from app.models.reservation import Reservation


def Get_reservations():
    reservation = Reservation.query.all()
    response = [
        {
            "id": r.id,
            "client_name": r.client_name,
            "people_quantity": r.people_quantity,
            "table_number": r.table_number,
            "booking_date": r.booking_date,
            "initial_time": r.initial_time.isoformat(),
            "final_time": r.final_time.isoformat(),
        }
        for r in reservation
    ]
    return jsonify(response)
