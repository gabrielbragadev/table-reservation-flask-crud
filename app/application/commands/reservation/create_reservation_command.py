from dataclasses import dataclass

from app.application.dtos.reservation.create_reservation_dto import (
    CreateReservationDTO,
)


@dataclass(frozen=True)
class CreateReservationCommand:
    data: CreateReservationDTO
