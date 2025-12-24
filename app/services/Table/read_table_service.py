from app.models.table import Table
from flask import jsonify


def get_table_service(table_id):
    tables = Table.query.filter_by(id=table_id).first()

    if not tables:
        return jsonify({"message": "Registro não encontrado"}), 404
    return jsonify(tables.to_dict())
