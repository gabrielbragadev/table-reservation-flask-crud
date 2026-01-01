from flask import abort, jsonify

from app.extensions import db
from app.models.reservation import Reservation
from app.services.Global.calculate_status_service import calculate_status


def delete_reservation_service(reservation_id):

    reservation = Reservation.query.filter_by(id=reservation_id).first()

    if reservation == None:
        abort(404, description="Reserva não encontrada")

    if reservation.table:
        reservation.table.status = "Available"

    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Reserva cancelada com sucesso"}), 200
