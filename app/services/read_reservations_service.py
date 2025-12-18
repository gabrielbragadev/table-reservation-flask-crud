from flask import jsonify
from app.models.reservation import Reservation
from app.extensions import db


def Get_reservations():
    reservation = Reservation.query.all()
    response = [
        {
            "id": r.id,
            "client_name": r.client_name,
            "table_number": r.table_number,
            "booking_date": r.booking_date.isoformat(),
            "initial_time": r.initial_time.isoformat(),
            "final_time": r.final_time.isoformat(),
        }
        for r in reservation
    ]
    return jsonify(response)
