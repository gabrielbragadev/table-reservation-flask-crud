from flask import Blueprint, request
from flask_login import login_required, current_user

from app.exceptions import ConflictError, UnauthorizedError

from app.schemas.reservation.reservation_create_schema import ReservationCreateSchema
from app.schemas.reservation.reservation_update_schema import ReservationUpdateSchema
from app.services.reservation.create_reservation_service import (
    create_reservation_service,
)
from app.services.reservation.read_reservations_service import get_reservations_service
from app.services.reservation.read_reservation_service import get_reservation_service
from app.services.reservation.update_reservation_service import (
    update_reservation_service,
)
from app.services.reservation.delete_reservation_service import (
    delete_reservation_service,
)

reservation_bp = Blueprint("reservation_bp", __name__, url_prefix="/reservations")


def register_reservation_routes(app):
    @app.route("/reservations", methods=["POST"])
    @login_required
    @app.route("/reservations", methods=["GET"])
    @login_required
    def reservations_read():
        return get_reservations_service()

    @app.route("/reservations/<int:reservation_id>", methods=["GET"])
    @login_required
    def reservation_read(reservation_id):
        return get_reservation_service(reservation_id)

    @app.route("/reservations/<int:reservation_id>", methods=["PUT"])
    @login_required
    def reservation_edit(reservation_id):
        data = ReservationUpdateSchema().load(request.get_json())
        return update_reservation_service(data, reservation_id)
