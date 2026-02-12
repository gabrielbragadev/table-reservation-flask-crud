from flask import jsonify, request
from flask_login import login_required
from app.application.services.table.create_table_service import CreateTableService
from app.interfaces.http.controllers.table_controllers import tables_bp
from app.interfaces.http.controllers.table_controllers.factories.create_table_factory import (
    create_table_factory,
)
from app.interfaces.http.schemas.table.create_table_schema import CreateTableSchema


@tables_bp.route("", methods=["POST"])
@login_required
def create_table():

    data = CreateTableSchema().load(request.get_json())
    factory = create_table_factory(data)

    service = CreateTableService(factory["table_repository"], factory["unit_of_work"])
    response = service.to_execute(factory["command"])

    return (
        jsonify(
            {
                "message": "Mesa cadastrada com sucesso.",
                "data": {
                    "id": response.id,
                    "table_number": response.table_number,
                    "people_capacity": response.people_capacity,
                },
            }
        ),
        201,
    )
