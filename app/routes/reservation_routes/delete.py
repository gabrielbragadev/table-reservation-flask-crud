from flask import jsonify
from flask_login import login_required

from app.exceptions import NotFoundError
from app.services.reservation.cancel_reservation_service import (
    cancel_reservation_service,
)

from app.routes.reservation_routes import reservations_bp


@reservations_bp.route("/<int:reservation_id>", methods=["DELETE"])
@login_required
def delete_reservation(reservation_id):
    try:
        cancel_reservation_service(reservation_id)
        return jsonify({"message": "Reserva cancelada com sucesso"}), 204
    except NotFoundError as error:
        return jsonify({"error": str(error)})
