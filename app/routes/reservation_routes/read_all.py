from flask import jsonify
from flask_login import login_required


from app.exceptions import NotFoundError
from app.services.reservation.read_reservations_service import GetReservationsService

from app.routes.reservation_routes import reservations_bp
from app.extensions import db


@reservations_bp.route("/", methods=["GET"])
@login_required
def get_reservations():
    try:
        service = GetReservationsService(db.session)
        reservations = service.to_execute()
        return jsonify(reservations), 200
    except NotFoundError as error:
        return jsonify({"error": str(error)})
