from typing import Dict
from flask_login import current_user
from app.application.commands.reservation.cancel_reservation_command import (
    CancelReservationCommand,
)
from app.infrastructure.persistence.sqlalchemy.reservation_repository import (
    ReservationRepository,
)
from app.infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository
from app.infrastructure.extensions import db


def cancel_factory(reservation_id: int) -> dict:
    reservation_repository = ReservationRepository(db.session)
    user_repository = UserRepository(db.session)
    unit_of_work = SqlAlchemyUnitOfWork(db.session)

    requester = user_repository.find_by_id(current_user.id)

    command = CancelReservationCommand(
        reservation_id=reservation_id,
        requester_user_id=requester.id,
        requester_role=requester.role,
    )

    return {
        "reservation_repository": reservation_repository,
        "unit_of_work": unit_of_work,
        "command": command,
    }
