from typing import Dict
from flask_login import current_user
from app.application.commands.reservation.read_reservation_command import (
    ReadReservationCommand,
)
from app.application.dtos.reservation.read_reservation_dto import ReadReservationDTO
from app.infrastructure.persistence.sqlalchemy.reservation_repository import (
    ReservationRepository,
)
from app.infrastructure.extensions import db
from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository


def read_factory(reservation_id: int) -> Dict[object]:

    reservation_repository = ReservationRepository(db.session)
    user_repository = UserRepository(db.session)
    dto = ReadReservationDTO(reservation_id)

    requester = user_repository.find_by_id(user_id=current_user.id)
    command = ReadReservationCommand(
        requester_role=requester.role, requester_user_id=requester.id, dto=dto
    )

    return {
        "reservation_repository": reservation_repository,
        "dto": dto.to_dict(),
        "command": command,
    }
