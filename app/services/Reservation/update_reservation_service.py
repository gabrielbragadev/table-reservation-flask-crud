from datetime import datetime

from flask import jsonify, request

from ...extensions import db
from ...models.reservation import Reservation


def update_reservation_service(data, id):
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
            
        reservation.table_number = table_number
        reservation.people_quantity = people_quantity
        reservation.booking_date = booking_date
        reservation.initial_time = initial_time
        reservation.final_time = final_time

    db.session.commit()
    return jsonify({"message": "Reserva Atualizada Com Sucesso"})
