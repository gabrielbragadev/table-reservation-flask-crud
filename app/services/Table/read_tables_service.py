from flask_login import current_user
from app.models.table import Table
from flask import jsonify

from app.models.user import User


def get_tables_service():

    authenticated_user = User.query.filter_by(id=current_user.id).first()
    if authenticated_user.role == "user":
        return jsonify({"message": "Usuário não autorizado"})

    tables = Table.query.all()

    if not tables:
        return jsonify({"message": "Registros não encontrados"}), 404

    response = [t.to_dict() for t in tables]
    return jsonify(response)
