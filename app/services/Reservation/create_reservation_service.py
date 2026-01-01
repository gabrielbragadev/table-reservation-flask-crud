from datetime import date, datetime

from flask import abort, jsonify

from app.exceptions import ConflictError
from app.extensions import db
from app.models.reservation import Reservation
from app.models.table import Table
from app.services.Global.calculate_status_service import calculate_status


def create_reservation_service(data):

    client_name = data.get("client_name")
    people_quantity = data.get("people_quantity")
    table_number = data.get("table_number")
    booking_date = data.get("booking_date")
    initial_time = data.get("initial_time")
    final_time = data.get("final_time")

    all_reservations = Reservation.query.all()
    table = Table.query.filter_by(table_number=table_number).first()

    if all_reservations is None:
        reservation = Reservation(
            client_name=client_name,
            people_quantity=people_quantity,
            table_number=table.table_number,
            booking_date=booking_date,
            initial_time=initial_time,
            final_time=final_time,
        )

        table.status = calculate_status(booking_date, initial_time)

        db.session.add(reservation)
        db.session.commit()
        return jsonify({"message": "Reserva Realizada Com Sucesso"})
    
    
    if table is None:
        abort(404, description="Mesa não encontrada")

    reservation_filter_by = Reservation.query.filter_by(
        table_number=table_number, booking_date=booking_date
    ).all()

    for r in reservation_filter_by:

        if not (final_time <= r.initial_time or initial_time >= r.final_time):
            raise ConflictError(message="Já existe reserva agendada para esse horario!")
        if people_quantity > r.table.people_capacity:
            raise ConflictError(
                message="Quantidade de pessoas acima da capacidade da mesa!"
            )

    reservation = Reservation(
        client_name=client_name,
        people_quantity=people_quantity,
        table_number=table.table_number,
        booking_date=booking_date,
        initial_time=initial_time,
        final_time=final_time,
    )

    table.status = calculate_status(booking_date, initial_time)

    db.session.add(reservation)
    db.session.commit()
    return jsonify({"message": "Reserva Realizada Com Sucesso"})
