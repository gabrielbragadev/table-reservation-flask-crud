from flask import jsonify
from flask_login import login_required


from app.exceptions import NotFoundError
from app.extensions import db
from app.services.reservation.read_reservation_service import GetReservationService

from app.routes.reservation_routes import reservations_bp


@reservations_bp.route("/<int:reservation_id>", methods=["GET"])
@login_required
def get_reservation(reservation_id):
    try:
        service = GetReservationService(reservation_id, db.session)
        reservation = service.to_execute()
        return jsonify(reservation), 200
    except NotFoundError as error:
        return jsonify({"error": str(error)})
