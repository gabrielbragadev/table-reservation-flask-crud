from app.models.table import Table
from app.extensions import db
from flask import jsonify


def Create_table_service(data):
    table_number = data.get("table_number")
    people_capacity = data.get("people_capacity")

    all_tables = Table.query.all()

    for t in all_tables:
        if table_number == t.table_number:
            return (
                jsonify({"message": "Já existe uma mesa cadastrada com esse número"}),
                409,
            )

    table = Table(table_number=table_number, people_capacity=people_capacity)
    db.session.add(table)
    db.session.commit()
    return jsonify({"message": "Mesa cadastrada com sucesso"})
