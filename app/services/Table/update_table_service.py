from flask import jsonify
from app.extensions import db
from app.models.table import Table


def update_table(data, table_id):

    table_number = data.get("table_number")
    people_capacity = data.get("people_capacity")

    if not table_number or not people_capacity:
        return (
            jsonify(
                {
                    "message": "Falha na validação dos dados. Campos obrigatórios ausentes ou inválidos."
                }
            ),
            422,
        )

    table = Table.query.filter_by(id=table_id).first()

    if not table:
        return jsonify({"message": "Registro não encontrado"}), 404

    table.table_number = table_number
    table.people_capacity = people_capacity

    db.session.commit()

    return jsonify({"message": "Registro alterado com sucesso"})
