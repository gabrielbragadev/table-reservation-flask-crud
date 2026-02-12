from flask import jsonify
from flask_login import current_user, login_required


from app.application.commands.reservation.read_reservation_command import (
    ReadReservationCommand,
)
from app.infrastructure.extensions import db
from app.application.services.reservation.read_reservation_service import (
    GetReservationService,
)

from app.infrastructure.persistence.sqlalchemy.reservation_repository import (
    ReservationRepository,
)
from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository
from app.interfaces.http.controllers.reservation_controllers import reservations_bp
from app.application.dtos.reservation.read_reservation_dto import ReadReservationDTO
from app.infrastructure.extensions import db


@reservations_bp.route("/<int:reservation_id>", methods=["GET"])
@login_required
def get_reservation(reservation_id):

    reservation_repository = ReservationRepository(db.session)
    user_repository = UserRepository(db.session)

    requester = user_repository.find_by_id(current_user.id)
    command = ReadReservationCommand(reservation_id, requester.role, requester.id)

    service = GetReservationService(reservation_repository)
    response = service.to_execute(command)

    dto = ReadReservationDTO(
        command.reservation_id,
        response["client_name"],
        response["people_quantity"],
        response["table_number"],
        response["booking_date"],
        response["initial_time"],
        response["final_time"],
        response["status"],
    )

    return jsonify(dto.to_dict()), 200
