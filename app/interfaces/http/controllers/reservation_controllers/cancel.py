from flask import jsonify
from flask_login import login_required

from app.application.services.reservation.cancel_reservation_service import (
    CancelReservationService,
)
from app.interfaces.http.controllers.reservation_controllers import reservations_bp
from app.interfaces.http.controllers.reservation_controllers.factories.cancel_factory import (
    cancel_factory,
)


@reservations_bp.route("/<int:reservation_id>", methods=["DELETE"])
@login_required
def delete_reservation(reservation_id):

    factory = cancel_factory(reservation_id=reservation_id)

    service = CancelReservationService(
        reservation_repository=factory["reservation_repository"],
        unit_of_work=factory["unit_of_work"],
    )
    service.to_execute(command=factory["command"])
    return jsonify({"message": "Reserva cancelada com sucesso"}), 204
