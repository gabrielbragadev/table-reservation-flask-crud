from flask_login import current_user
from app.extensions import db
from app.models.table import Table
from flask import jsonify

from app.models.user import User


def delete_table_service(table_id):

    authenticated_user = User.query.filter_by(id=current_user.id).first()
    if authenticated_user.role == "user":
        return jsonify({"message": "Usuário não autorizado"})

    table = Table.query.filter_by(id=table_id).first()

    if not table:
        return jsonify({"message": "Registro não encontrado"})

    db.session.delete(table)
    db.session.commit()

    return jsonify({"message": "Registro excluído com sucesso"})
