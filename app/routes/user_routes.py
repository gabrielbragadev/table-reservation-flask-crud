from flask import request
from flask_login import login_required

from app.schemas.User.user_create_schema import UserCreateSchema
from app.schemas.User.user_update_schema import UserUpdateSchema
from app.services.User.create_user_service import create_user_service
from app.services.User.read_users_service import get_users_service
from app.services.User.update_user_service import update_user
from app.services.User.delete_user_service import delete_user


def register_user_routes(app):
    @app.route("/users", methods=["POST"])
    def user_create():
        data = UserCreateSchema().load(request.get_json())
        return create_user_service(data)

    @app.route("/users", methods=["GET"])
    @login_required
    def user_read():
        return get_users_service()

    @app.route("/users/<int:user_id>", methods=["PUT"])
    @login_required
    def user_update_route(user_id):
        data = UserUpdateSchema().load(request.get_json())
        return update_user(data, user_id)

    @app.route("/users/<int:user_id>", methods=["DELETE"])
    @login_required
    def user_delete_route(user_id):
        return delete_user(user_id)
