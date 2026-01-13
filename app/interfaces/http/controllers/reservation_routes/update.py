from flask import jsonify, request
from flask_login import login_required
from app.domains.exceptions import NotFoundError
from app.interfaces.http.controllers.reservation_routes import reservations_bp
from app.application.services.reservation.update_reservation_service import (
    update_reservation_service,
)
from app.interfaces.http.schemas.reservation.reservation_update_schema import ReservationUpdateSchema


@reservations_bp.route("/<int:reservation_id>", methods=["PUT"])
@login_required
def update_reservation(reservation_id: int):
    data = ReservationUpdateSchema().load(request.get_json())

    try:
        updated_reservation = update_reservation_service(data, reservation_id)
        return jsonify(
            {
                "message": "Reserva atualizada com sucesso",
                "reserva pós alteração:": updated_reservation,
            }
        )
    except NotFoundError as error:
        return jsonify({"error": error.message}), 404
