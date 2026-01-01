from flask import abort, jsonify

from app.models.reservation import Reservation


def get_reservation_service(reservation_id):

    reservation = Reservation.query.filter_by(id=reservation_id).first()
    if not reservation:
        abort(404, description="Reserva não encontrada")

    return jsonify(reservation.to_dict())
