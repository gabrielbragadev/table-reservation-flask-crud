from typing import Dict
from flask import request
from flask_login import current_user
from app.application.commands.reservation.update_reservation_command import (
    UpdateReservationCommand,
)
from app.application.dtos.reservation.update_reservation_dto import UpdateReservationDTO
from app.domain.repositories.table_repository import TableRepository
from app.domain.services.reservation.reservation_conflict_checker import (
    ReservationConflictChecker,
)
from app.domain.services.reservation.reservation_table_provider import (
    ReservationTableProvider,
)
from app.infrastructure.persistence.sqlalchemy.reservation_repository import (
    ReservationRepository,
)
from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository
from app.interfaces.http.schemas.reservation.reservation_update_schema import (
    ReservationUpdateSchema,
)
from app.infrastructure.extensions import db
from app.infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork


def update_factory(reservation_id: int) -> dict:
    data = ReservationUpdateSchema().load(request.get_json())

    reservation_repository = ReservationRepository(db.session)
    table_repository = TableRepository()
    user_repository = UserRepository(db.session)

    conflict_checker = ReservationConflictChecker(reservation_repository)
    reservation_table_provider = ReservationTableProvider(table_repository)
    unit_of_work = SqlAlchemyUnitOfWork(db.session)

    requester = user_repository.find_by_id(current_user.id)

    dto = UpdateReservationDTO(
        people_quantity=data.get("people_quantity"),
        table_number=data.get("table_number"),
        booking_date=data.get("booking_date"),
        initial_time=data.get("initial_time"),
        final_time=data.get("final_time"),
    )

    command = UpdateReservationCommand(
        reservation_id=reservation_id,
        dto=dto,
        requester_user_id=requester.id,
        requester_role=requester.role,
    )

    return {
        "reservation_repository": reservation_repository,
        "conflict_checker": conflict_checker,
        "reservation_table_provider": reservation_table_provider,
        "unit_of_work": unit_of_work,
        "command": command,
    }
