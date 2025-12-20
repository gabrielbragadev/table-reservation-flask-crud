from ...models.reservation import Reservation
from flask import request, jsonify
from ...extensions import db
from datetime import datetime


def Update_reservation(data, id):

    reservation = Reservation.query.filter_by(id=id).first()

    reservation.table_number = data.get("table_number")
    reservation.booking_date = data.get("booking_date")
    reservation.initial_time = data.get("initial_time")
    reservation.final_time = data.get("final_time")

    db.session.commit()
    return jsonify({"message": "Reserva Atualizada Com Sucesso"})
