from flask import Flask, request, jsonify
from models.reservation import Reservation
from datetime import datetime


reservations = []
app = Flask(__name__)
id = 1


@app.route("/reservations", methods=["POST"])
def create_reservation():
    global id
    data = request.get_json()
    initial_data_time = data["initial_time"]
    final_data_time = data["final_time"]
    initial_date_time = datetime.strptime(initial_data_time, "%Y-%m-%dT%H:%M:%S")
    final_date_time = datetime.strptime(final_data_time, "%Y-%m-%dT%H:%M:%S")
    for r in reservations:
        if data["table_number"] == r.table_number:
            if (
                initial_date_time <= r.final_time
                and initial_date_time >= r.initial_time
            ):
                return jsonify({"message": "Horário já reservado!"}), 404
    new_reservation = Reservation(
        client_name=data["client_name"],
        table_number=data["table_number"],
        initial_time=initial_date_time,
        final_time=final_date_time,
        id_reservation=id,
    )
    reservations.append(new_reservation)
    id += 1
    return jsonify({"message": "Reserva feita com sucesso"}), 200


@app.route("/reservations", methods=["GET"])
def get_reservations():
    reservation_list = [r.to_dict() for r in reservations]
    output = {
        "reservations": reservation_list,
        "total_reservations": len(reservation_list),
    }
    return jsonify(output)


@app.route("/reservations/<int:id_reservation>", methods=["GET"])
def get_reservation(id_reservation):
    for r in reservations:
        if r.id_reservation == id_reservation:
            return jsonify(r.to_dict())

    return jsonify({"message": "Reserva Não encontrada"}), 404


if __name__ == "__main__":
    app.run(debug=True)
