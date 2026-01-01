from flask import request
from flask_login import login_required

from app.schemas.Table.create_table_schema import CreateTableSchema
from app.schemas.Table.update_table_schema import UpdateTableSchema
from app.services.Table.create_table_service import create_table_service
from app.services.Table.read_tables_service import get_tables_service
from app.services.Table.read_table_service import get_table_service
from app.services.Table.update_table_service import update_table
from app.services.Table.delete_table_service import delete_table_service


def register_table_routes(app):
    @app.route("/tables", methods=["POST"])
    @login_required
    def table_create():
        data = CreateTableSchema().load(request.get_json())
        return create_table_service(data)

    @app.route("/tables", methods=["GET"])
    @login_required
    def tables_read():
        return get_tables_service()

    @app.route("/tables/<int:table_id>", methods=["GET"])
    @login_required
    def table_read(table_id):
        return get_table_service(table_id)

    @app.route("/tables/<int:table_id>", methods=["PUT"])
    @login_required
    def table_update_route(table_id):
        data = UpdateTableSchema().load(request.get_json())
        return update_table(data, table_id)

    @app.route("/tables/<int:table_id>", methods=["DELETE"])
    @login_required
    def table_delete_route(table_id):
        return delete_table_service(table_id)
