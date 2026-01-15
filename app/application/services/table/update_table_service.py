from flask import jsonify, abort
from flask_login import current_user
from app.domain.exceptions import ConflictError
from app.infrastructure.extensions import db
from app.domain.entities.reservation import Reservation
from app.domain.entities.table import Table
from app.domain.entities.user import User


def update_table(data, table_id):

    authenticated_user = User.query.filter_by(id=current_user.id).first()
    if authenticated_user.role == "user":
        abort(403)

    table_number = data.get("table_number")
    people_capacity = data.get("people_capacity")

    if not table_number or not people_capacity:
        abort(422)

    all_tables = Table.query.all()

    for t in all_tables:
        if table_number == t.table_number:
            raise ConflictError(message="Já existe uma mesa cadastrada com esse número")

    table = Table.query.filter_by(id=table_id).first()

    if not table:
        abort(404)

    existing_reservation = Reservation.query.filter_by(
        table_number=table.table_number
    ).first()
    if existing_reservation:
        raise ConflictError(
            "Não é possível editar a mesa porque existem reservas vinculadas a ela"
        )

    if table_number:
        table.table_number = table_number
    if people_capacity:
        table.people_capacity = people_capacity

    db.session.commit()

    return jsonify({"message": "Registro alterado com sucesso"})
