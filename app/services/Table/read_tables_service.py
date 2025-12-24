from app.models.table import Table
from flask import jsonify


def get_tables_service():
    tables = Table.query.all()

    if not tables:
        return jsonify({"message": "Registros não encontrados"}), 404

    response = [t.to_dict() for t in tables]
    return jsonify(response)
