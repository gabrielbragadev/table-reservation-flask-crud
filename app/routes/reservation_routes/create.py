from flask import request, jsonify
from flask_login import current_user, login_required

from app.exceptions import ConflictError, UnauthorizedError
from app.services.reservation.create_reservation_service import (
    create_reservation_service,
)
from app.schemas.reservation.reservation_create_schema import ReservationCreateSchema
from app.routes.reservation_routes import reservations_bp


@reservations_bp.route("/", methods=["POST"])
def create_reservation():

    data = ReservationCreateSchema().load(request.get_json())
    user_authenticated = current_user.is_authenticated if current_user else False

    try:
        create_reservation_service(data, user_authenticated)
        return jsonify({"message": "Reserva realizada com sucesso"}), 201
    except ValueError as error:
        return jsonify({"error": str(error.message)}), 404
    except UnauthorizedError as error:
        return jsonify({"error": error.message}), 401
    except ConflictError as error:
        return jsonify({"error": error.message}), 409
    except Exception as error:
        return jsonify({"error": str(error)}), 500
