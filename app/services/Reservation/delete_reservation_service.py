from flask import jsonify

from app.extensions import db
from app.models.reservation import Reservation


def delete_reservation_service(reservation_id):
    
    reservation = Reservation.query.filter_by(id=reservation_id).first()
    if reservation == None:
        return jsonify({"message": "Reserva não encontrada"}), 404
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Reserva cancelada com sucesso"}), 200
