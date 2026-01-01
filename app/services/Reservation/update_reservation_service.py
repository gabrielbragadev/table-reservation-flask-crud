from datetime import datetime
from flask import abort, jsonify

from app.exceptions import ConflictError
from app.models.table import Table
from app.services.Global.calculate_status_service import calculate_status
from app.extensions import db
from app.models.reservation import Reservation


def update_reservation_service(data, id):
    table_number = data.get("table_number")
    people_quantity = data.get("people_quantity")
    booking_date = data.get("booking_date")
    initial_time = data.get("initial_time")
    final_time = data.get("final_time")

    new_table = Table.query.filter_by(table_number=table_number).first()
    if not new_table:
        abort(404, description="Mesa não encontrada")

    reservation = Reservation.query.filter_by(id=id).first()
    if not reservation:
        abort(404, description="Reserva não encontrada")

    old_table = Table.query.filter_by(table_number=reservation.table_number).first()

    reservation_filter_by = Reservation.query.filter_by(
        table_number=table_number, booking_date=booking_date
    ).all()

    for r in reservation_filter_by:

        if not (final_time <= r.initial_time or initial_time >= r.final_time):
            raise ConflictError(message="Já existe reserva agendada para esse horário")

        if people_quantity and people_quantity > new_table.people_capacity:
            raise ConflictError("Quantidade de pessoas acima da capacidade da mesa")

    if old_table.status == "Reserved":
        old_table.status = "Available"

    if table_number:
        reservation.table_number = new_table.table_number
    if people_quantity:
        reservation.people_quantity = people_quantity
    if booking_date:
        reservation.booking_date = booking_date
    if initial_time:
        reservation.initial_time = initial_time
    if final_time:
        reservation.final_time = final_time

    new_table.status = calculate_status(booking_date, initial_time)

    db.session.commit()
    return jsonify({"message": "Reserva Atualizada Com Sucesso"})
