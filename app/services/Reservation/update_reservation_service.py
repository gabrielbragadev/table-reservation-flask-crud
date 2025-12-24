from datetime import datetime

from flask import jsonify, request

from ...extensions import db
from ...models.reservation import Reservation


def Update_reservation(data, id):
    table_number = data.get("table_number")
    people_quantity = data.get("people_quantity")
    booking_date = data.get("booking_date")
    initial_time = data.get("initial_time")
    final_time = data.get("final_time")

    reservation = Reservation.query.filter_by(id=id).first()
    reservation_filter_by = Reservation.query.filter_by(
        table_number=table_number, booking_date=booking_date
    ).all()

    for r in reservation_filter_by:

        if not (final_time <= r.initial_time or initial_time >= r.final_time):
            return (
                jsonify({"message": "Já existe reserva agendada para esse horario!"}),
                409,
            )

        if people_quantity and people_quantity > r.table.people_capacity:
            return (
                jsonify(
                    {"message": "Quantidade de pessoas acima da capacidade da mesa"}
                ),
                409,
            )
    if table_number:
        reservation.table_number = table_number
    if people_quantity:
        reservation.people_quantity = people_quantity
    if booking_date:
        reservation.booking_date = booking_date
    if initial_time:
        reservation.initial_time = initial_time
    if final_time:
        reservation.final_time = final_time

    db.session.commit()
    return jsonify({"message": "Reserva Atualizada Com Sucesso"})
