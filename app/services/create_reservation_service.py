from flask import jsonify
from app.models.reservation import Reservation
from app.extensions import db
from datetime import datetime


def CreateReservation(data):

    client_name = data.get("client_name")
    table_number = data.get("table_number")
    booking_date = data.get("booking_date")
    initial_time = data.get("initial_time")
    final_time = data.get("final_time")

    booking_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
    initial_time = datetime.strptime(initial_time, "%H:%M:%S").time()
    final_time = datetime.strptime(final_time, "%H:%M:%S").time()

    if (
        not client_name
        or not table_number
        or not booking_date
        or not initial_time
        or not final_time
    ):
        return jsonify({"message": "Os dados não foram totalmente preenchidos"}), 400

    if initial_time > final_time:
        return (
            jsonify(
                {"message": "Horário de ínicio não pode ser maior que o horário final."}
            )
        ), 409

    all_reservations = Reservation.query.all()
    if not all_reservations:
        reservation = Reservation(
            client_name=client_name,
            table_number=table_number,
            booking_date=booking_date,
            initial_time=initial_time,
            final_time=final_time,
        )

        db.session.add(reservation)
        db.session.commit()
        return jsonify({"message": "Reserva Realizada Com Sucesso"})

    reservation_filter_by = Reservation.query.filter_by(
        table_number=table_number,
        booking_date=booking_date,
        initial_time=initial_time,
        final_time=final_time,
    ).all()

    for r in reservation_filter_by:

        if final_time <= r.initial_time or initial_time >= final_time:

            reservation = Reservation(
                client_name=client_name,
                table_number=table_number,
                booking_date=booking_date,
                initial_time=initial_time,
                final_time=final_time,
            )

            db.session.add(reservation)
            db.session.commit()
            return jsonify("message", "Reserva Realizada Com Sucesso")

    return jsonify({"message": "Já existe reserva agendada para esse horario!"}), 409
