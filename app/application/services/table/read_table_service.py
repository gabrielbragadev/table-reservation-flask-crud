from flask_login import current_user
from app.domain.entities.table import Table
from flask import abort, jsonify

from app.domain.entities.user import User


def get_table_service(table_id):

    authenticated_user = User.query.filter_by(id=current_user.id).first()
    if authenticated_user.role == "user":
        abort(403)

    tables = Table.query.filter_by(id=table_id).first()

    if not tables:
        abort(404)
    return jsonify(tables.to_dict())
