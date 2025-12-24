from flask import jsonify

from app.models.reservation import Reservation


def get_reservations_service():
    reservations = Reservation.query.all()
    if not reservations:
        return jsonify({"message": "Nenhum registro encontrado"}), 404
    response = [r.to_dict() for r in reservations]
    return jsonify(response)
