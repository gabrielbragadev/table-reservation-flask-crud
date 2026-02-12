from flask_login import current_user
from app.domain.exceptions import ConflictError
from app.infrastructure.extensions import db
from app.domain.entities.table import Table
from app.domain.entities.reservation import Reservation
from flask import abort, jsonify

from app.domain.entities.user import User


def delete_table_service(table_id):

    authenticated_user = User.query.filter_by(id=current_user.id).first()
    if authenticated_user.role == "user":
        abort(403)

    table = Table.query.filter_by(id=table_id).first()

    if not table:
        abort(404)

    existing_reservation = Reservation.query.filter_by(
        table_number=table.table_number
    ).first()
    if existing_reservation:
        raise ConflictError(
            "Não é possível excluir a mesa porque existem reservas vinculadas a ela"
        )

    db.session.delete(table)
    db.session.commit()

    return jsonify({"message": "Registro excluído com sucesso"})
