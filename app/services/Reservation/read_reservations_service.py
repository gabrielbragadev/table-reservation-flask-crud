from flask import abort, jsonify

from app.models.reservation import Reservation


def get_reservations_service():
    reservations = Reservation.query.all()
    if not reservations:
        abort(404, description="Nenhum registro encontrado!")
    response = [r.to_dict() for r in reservations]
    return jsonify(response)
