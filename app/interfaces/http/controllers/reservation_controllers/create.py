from flask import request, jsonify
from flask_login import login_required
from app.application.commands.reservation.create_reservation_command import (
    CreateReservationCommand,
)
from app.application.dtos.reservation.create_reservation_dto import CreateReservationDTO
from app.infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.persistence.sqlalchemy.table_repository import TableRepository
from app.domain.services.reservation.reservation_conflict_checker import (
    ReservationConflictChecker,
)
from app.domain.services.reservation.reservation_table_provider import (
    ReservationTableProvider,
)
from app.infrastructure.extensions import db

from app.application.services.reservation.create_reservation_service import (
    CreateReservationService,
)
from app.interfaces.http.schemas.reservation.reservation_create_schema import (
    ReservationCreateSchema,
)
from app.interfaces.http.controllers.reservation_controllers import reservations_bp
from app.infrastructure.persistence.sqlalchemy.reservation_repository import (
    ReservationRepository,
)
from app.interfaces.http.controllers.reservation_controllers.factories.create_factory import (
    create_factory,
)


@reservations_bp.route("/", methods=["POST"])
@login_required
def create_reservation():

    factory = create_factory()

    service = CreateReservationService(
        factory["reservation_repository"],
        factory["conflict_checker_service"],
        factory["reservation_table_provider"],
        factory["unit_of_work"],
    )
    service.to_execute(factory["command"])
    return jsonify({"message": "Reserva realizada com sucesso"}), 201
