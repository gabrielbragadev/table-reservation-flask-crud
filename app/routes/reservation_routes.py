from flask import request
from flask_login import login_required

from app.schemas.Reservation.reservation_create_schema import ReservationCreateSchema
from app.schemas.Reservation.reservation_update_schema import ReservationUpdateSchema
from app.services.Reservation.create_reservation_service import create_reservation_service
from app.services.Reservation.read_reservations_service import get_reservations_service
from app.services.Reservation.read_reservation_service import get_reservation_service
from app.services.Reservation.update_reservation_service import update_reservation_service
from app.services.Reservation.delete_reservation_service import delete_reservation_service


def register_reservation_routes(app):
    @app.route("/reservations", methods=["POST"])
    @login_required
    def reservation_create():
        data = ReservationCreateSchema().load(request.get_json())
        return create_reservation_service(data)

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

    @app.route("/reservations/<int:reservation_id>", methods=["DELETE"])
    @login_required
    def reservation_cancellation(reservation_id):
        return delete_reservation_service(reservation_id)
