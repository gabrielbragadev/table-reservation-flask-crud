from flask import jsonify
from app.models.reservation import Reservation
from app.extensions import db
from datetime import datetime


def CreateReservation(data):
    data["booking_date"] = datetime.strptime(data["booking_date"], "%Y-%m-%d").date()
    data["initial_time"] = datetime.strptime(data["initial_time"], "%H:%M:%S").time()
    data["final_time"] = datetime.strptime(data["final_time"], "%H:%M:%S").time()

    if (
        data.get("client_name")
        and data.get("table_number")
        and data.get("booking_date")
        and data.get("initial_time")
        and data.get("final_time")
    ):

        reservation_filter_by = Reservation.query.filter_by(
            table_number=data["table_number"],
            booking_date=data["booking_date"],
            initial_time=data["initial_time"],
            final_time=data["final_time"],
        ).all()

        for r in reservation_filter_by:
            if not (
                data["final_time"] <= r.initial_time
                and data["initial_time"] >= r.final_time
            ):
                return jsonify(
                    {
                        "message": f"Já existe reserva agendada para o dia {data["booking_date"]} as {data["initial_time"]}"
                    },
                    409,
                )

        reservation = Reservation(**data)
        db.session.add(reservation)
        db.session.commit()
        return jsonify({"message": "Reserva cadastrada com sucesso"}), 201
    return jsonify({"message": "Os dados não foram totalmente preenchidos"}), 400
