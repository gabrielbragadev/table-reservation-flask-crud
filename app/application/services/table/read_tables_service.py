from flask_login import current_user
from app.domains.entities.table import Table
from flask import abort, jsonify

from app.domains.entities.user import User


def get_tables_service():

    authenticated_user = User.query.filter_by(id=current_user.id).first()
    if authenticated_user.role == "user":
        abort(403)

    tables = Table.query.all()

    if not tables:
        abort(404)

    response = [t.to_dict() for t in tables]
    return jsonify(response)
