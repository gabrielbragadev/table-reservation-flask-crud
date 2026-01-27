from typing import Dict
from flask_login import current_user
from app.application.commands.reservation.read_reservations_command import (
    ReadReservationsCommand,
)
from app.infrastructure.persistence.sqlalchemy.reservation_repository import (
    ReservationRepository,
)
from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository
from app.infrastructure.extensions import db


def read_all_factory() -> Dict[object]:
    reservation_repository = ReservationRepository(db.session)
    user_repository = UserRepository(db.session)

    requester = user_repository.find_by_id(current_user.id)

    command = ReadReservationsCommand(
        requester_role=requester.role, requester_user_id=requester.id
    )

    return {"reservation_repository": reservation_repository, "command": command}
