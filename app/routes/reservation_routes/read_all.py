from flask import jsonify
from flask_login import login_required


from app.exceptions import NotFoundError
from app.services.reservation.read_reservations_service import get_reservations_service

from app.routes.reservation_routes import reservations_bp


@reservations_bp.route("/", methods=["GET"])
@login_required
def get_reservations():
    try:
        reservations = get_reservations_service()
        return jsonify(reservations), 200
    except NotFoundError as error:
        return jsonify({"error": str(error)})
