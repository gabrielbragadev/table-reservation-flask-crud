from flask_login import current_user
from app.models.table import Table
from flask import jsonify

from app.models.user import User


def get_table_service(table_id):
    
    authenticated_user = User.query.filter_by(id=current_user.id).first()
    if authenticated_user.role == "user":
        return jsonify({"message": "Usuário não autorizado"})
    
    tables = Table.query.filter_by(id=table_id).first()

    if not tables:
        return jsonify({"message": "Registro não encontrado"}), 404
    return jsonify(tables.to_dict())
