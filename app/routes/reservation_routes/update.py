from flask import jsonify, request
from flask_login import login_required
from app.exceptions import NotFoundError
from app.routes.reservation_routes import reservations_bp
from app.services.reservation.update_reservation_service import (
    update_reservation_service,
)
from app.schemas.reservation.reservation_update_schema import ReservationUpdateSchema


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
