from flask import jsonify
from app.models.reservation import Reservation
from app.extensions import db


def CreateReservation(data):

    client_name = data.get("client_name")
    people_quantity = data.get("people_quantity")
    table_number = data.get("table_number")
    booking_date = data.get("booking_date")
    initial_time = data.get("initial_time")
    final_time = data.get("final_time")

    all_reservations = Reservation.query.all()
    if not all_reservations:
        reservation = Reservation(
            client_name=client_name,
            people_quantity=people_quantity,
            table_number=table_number,
            booking_date=booking_date,
            initial_time=initial_time,
            final_time=final_time,
        )

        db.session.add(reservation)
        db.session.commit()
        return jsonify({"message": "Reserva Realizada Com Sucesso"})

    reservation_filter_by = Reservation.query.filter_by(
        table_number=table_number, booking_date=booking_date
    ).all()

    for r in reservation_filter_by:

        if not (final_time <= r.initial_time or initial_time >= r.final_time):
            return (
                jsonify({"message": "Já existe reserva agendada para esse horario!"}),
                409,
            )
        if people_quantity > r.table.people_capacity:
            return (
                jsonify(
                    {"message": "Quantidade de pessoas acima da capacidade da mesa"}
                ),
                409,
            )

    reservation = Reservation(
        client_name=client_name,
        people_quantity=people_quantity,
        table_number=table_number,
        booking_date=booking_date,
        initial_time=initial_time,
        final_time=final_time,
    )

    db.session.add(reservation)
    db.session.commit()
    return jsonify({"message": "Reserva Realizada Com Sucesso"})
