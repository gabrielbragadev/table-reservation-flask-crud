from flask import jsonify
from flask_login import login_required


from app.application.services.reservation.read_reservations_service import (
    GetReservationsService,
)
from app.interfaces.http.controllers.reservation_controllers import reservations_bp
from app.interfaces.http.controllers.reservation_controllers.factories.read_all_factory import (
    read_all_factory,
)


@reservations_bp.route("", methods=["GET"])
@login_required
def get_reservations():

    factory = read_all_factory()

    service = GetReservationsService(
        reservation_repository=factory["reservation_repository"]
    )
    reservations = service.to_execute(factory["command"])
    return jsonify(reservations), 200
