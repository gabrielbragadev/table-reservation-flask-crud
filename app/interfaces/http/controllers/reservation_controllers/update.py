from flask import jsonify
from flask_login import login_required
from app.interfaces.http.controllers.reservation_controllers import reservations_bp
from app.application.services.reservation.update_reservation_service import (
    UpdateReservationsService,
)
from app.interfaces.http.controllers.reservation_controllers.factories.update_factory import (
    update_factory,
)


@reservations_bp.route("/<int:reservation_id>", methods=["PUT"])
@login_required
def update_reservation(reservation_id: int):

    factory = update_factory(reservation_id)

    service = UpdateReservationsService(
        factory["reservation_repository"],
        factory["conflict_checker"],
        factory["reservation_table_provider"],
        factory["unit_of_work"],
    )

    updated_reservation = service.to_execute(factory["command"])
    return jsonify(
        {
            "message": "Reserva atualizada com sucesso",
            "reserva pós alteração:": updated_reservation,
        }
    )
