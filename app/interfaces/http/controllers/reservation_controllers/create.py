from flask import jsonify
from flask_login import login_required

from app.application.services.reservation.create_reservation_service import (
    CreateReservationService,
)

from app.interfaces.http.controllers.reservation_controllers import reservations_bp

from app.interfaces.http.controllers.reservation_controllers.factories.create_factory import (
    create_factory,
)


@reservations_bp.route("/", methods=["POST"])
@login_required
def create_reservation():

    factory = create_factory()

    service = CreateReservationService(
        factory["reservation_repository"],
        factory["conflict_checker_service"],
        factory["reservation_table_provider"],
        factory["unit_of_work"],
    )
    service.to_execute(factory["command"])
    return jsonify({"message": "Reserva realizada com sucesso"}), 201
