from flask import jsonify
from flask_login import login_required


from app.domain.exceptions import NotFoundError
from app.infrastructure.extensions import db
from app.application.services.reservation.read_reservation_service import (
    GetReservationService,
)

from app.interfaces.http.controllers.reservation_controllers import reservations_bp
from app.interfaces.http.controllers.reservation_controllers.factories.read_factory import (
    read_factory,
)
from app.application.dtos.reservation.read_reservation_dto import ReadReservationDTO


@reservations_bp.route("/<int:reservation_id>", methods=["GET"])
@login_required
def get_reservation(reservation_id):

    factory = read_factory(reservation_id)

    service = GetReservationService(factory["reservation_repository"])
    service.to_execute(factory["command"])

    return jsonify(factory["dto"]), 200
