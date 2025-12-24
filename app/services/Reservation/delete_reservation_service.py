from flask import jsonify

from ...extensions import db
from ...models.reservation import Reservation


def Delete_reservation(id):
    reservation = Reservation.query.filter_by(id=id).first()
    if reservation == None:
        return jsonify({"message": "Reserva não encontrada"}), 404
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Reserva cancelada com sucesso"}), 200
