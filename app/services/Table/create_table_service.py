from flask import abort, jsonify
from flask_login import current_user

from app.exceptions import ConflictError
from app.extensions import db
from app.models.user import User
from app.models.table import Table


def create_table_service(data):

    authenticated_user = User.query.filter_by(id=current_user.id).first()
    if authenticated_user.role == "user":
        abort(403)

    table_number = data.get("table_number")
    people_capacity = data.get("people_capacity")

    all_tables = Table.query.all()

    for t in all_tables:
        if table_number == t.table_number:
            raise ConflictError(message="Já existe uma mesa cadastrada com esse número")

    table = Table(table_number=table_number, people_capacity=people_capacity)
    db.session.add(table)
    db.session.commit()
    return jsonify({"message": "Mesa cadastrada com sucesso"})
