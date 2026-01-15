from flask import jsonify
from flask_login import login_required
from app.infrastructure.extensions import db

from app.domain.exceptions import NotFoundError
from app.application.services.reservation.cancel_reservation_service import CancelReservationService

from app.interfaces.http.controllers.reservation_controllers import reservations_bp


@reservations_bp.route("/<int:reservation_id>", methods=["DELETE"])
@login_required
def delete_reservation(reservation_id):
    try:
        service = CancelReservationService(reservation_id, db.session)
        service.to_execute()
        return jsonify({"message": "Reserva cancelada com sucesso"}), 204
    except NotFoundError as error:
        return jsonify({"error": str(error)})
