from ..models.reservation import Reservation
from flask import request, jsonify
from ..extensions import db
from datetime import datetime


def Update_reservation(data, id):
    date = datetime.strptime(data.get("booking_date"), "%Y-%m-%d").date()
    initial_time = datetime.strptime(data.get("initial_time"), "%H:%M:%S").time()
    final_time = datetime.strptime(data.get("final_time"), "%H:%M:%S").time()

    reservation = Reservation.query.filter_by(id=id).first()

    reservation.table_number = data["table_number"]
    reservation.booking_date = date
    reservation.initial_time = initial_time
    reservation.final_time = final_time

    db.session.commit()
    return jsonify({"message": "Reserva Atualizada Com Sucesso"})
