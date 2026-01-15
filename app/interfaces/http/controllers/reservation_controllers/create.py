from flask import request, jsonify
from flask_login import login_required
from app.infrastructure.extensions import db

from app.domain.exceptions import ConflictError, UnauthorizedError
from app.application.services.reservation.create_reservation_service import CreateReservationService
from app.interfaces.http.schemas.reservation.reservation_create_schema import ReservationCreateSchema
from app.interfaces.http.controllers.reservation_controllers import reservations_bp


@reservations_bp.route("/", methods=["POST"])
@login_required
def create_reservation():

    data = ReservationCreateSchema().load(request.get_json())
    

    try:
        service = CreateReservationService(data, db.session)
        service.to_execute()
        return jsonify({"message": "Reserva realizada com sucesso"}), 201
    except ValueError as error:
        return jsonify({"error": str(error.message)}), 404
    except UnauthorizedError as error:
        return jsonify({"error": error.message}), 401
    except ConflictError as error:
        return jsonify({"error": error.message}), 409
    except Exception as error:
        return jsonify({"error": str(error)}), 500
