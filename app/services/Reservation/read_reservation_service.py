from flask import jsonify

from app.models.reservation import Reservation


def get_reservation_service(reservation_id):
    
    reservation = Reservation.query.filter_by(id=reservation_id).first()
    if not reservation:
        return jsonify({"message": "Registro Inexistente"}), 404
    
    return jsonify(reservation.to_dict())
