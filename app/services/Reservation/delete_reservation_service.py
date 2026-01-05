from app.extensions import db
from app.exceptions import NotFoundError
from app.models.reservation import Reservation


def delete_reservation_service(reservation_id: int) -> None:
    reservation = __check_reservation_exists(reservation_id)
    __change_status(reservation_id)

    db.session.delete(reservation)
    db.session.commit()


def __get_reservation_to_be_deleted(reservation_id: int) -> Reservation:
    reservation = Reservation.query.filter_by(id=reservation_id).first()
    return reservation


def __check_reservation_exists(reservation_id: int) -> Reservation:

    reservation = __get_reservation_to_be_deleted(reservation_id)
    if reservation is None:
        raise NotFoundError(message="Reserva não encontrada")
    return reservation


def __change_status(reservation_id: int) -> None:
    reservation = __get_reservation_to_be_deleted(reservation_id)

    if reservation.table:
        reservation.table.status = "Available"
