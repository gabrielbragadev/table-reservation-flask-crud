from typing import Dict
from flask import request
from app.application.commands.reservation.create_reservation_command import (
    CreateReservationCommand,
)
from app.application.dtos.reservation.create_reservation_dto import CreateReservationDTO
from app.domain.services.reservation.reservation_conflict_checker import (
    ReservationConflictChecker,
)
from app.domain.services.reservation.reservation_table_provider import (
    ReservationTableProvider,
)
from app.infrastructure.persistence.sqlalchemy.reservation_repository import (
    ReservationRepository,
)
from app.infrastructure.persistence.sqlalchemy.table_repository import TableRepository
from app.infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork
from app.interfaces.http.schemas.reservation.reservation_create_schema import (
    ReservationCreateSchema,
)
from app.infrastructure.extensions import db


def create_factory() -> dict:

    data = ReservationCreateSchema().load(request.get_json())

    reservation_repository = ReservationRepository(db.session)
    table_repository = TableRepository(db.session)
    conflict_checker_service = ReservationConflictChecker(reservation_repository)
    reservation_table_provider = ReservationTableProvider(table_repository)
    unit_of_work = SqlAlchemyUnitOfWork(db.session)

    dto = CreateReservationDTO(
        data.get("client_name"),
        data.get("people_quantity"),
        data.get("table_number"),
        data.get("booking_date"),
        data.get("initial_time"),
        data.get("final_time"),
    )

    command = CreateReservationCommand(dto)

    return {
        "reservation_repository": reservation_repository,
        "conflict_checker_service": conflict_checker_service,
        "reservation_table_provider": reservation_table_provider,
        "unit_of_work": unit_of_work,
        "command": command,
    }
