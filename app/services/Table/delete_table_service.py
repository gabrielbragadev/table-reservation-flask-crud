from app.extensions import db
from app.models.table import Table
from flask import jsonify


def delete_table_service(table_id):
    table = Table.query.filter_by(id=table_id).first()

    if not table:
        return jsonify({"message": "Registro não encontrado"})

    db.session.delete(table)
    db.session.commit()

    return jsonify({"message": "Registro excluído com sucesso"})
