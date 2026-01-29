from flask import jsonify
from flask_login import login_required
from app.application.services.user.read_users_service import GetUsersService
from app.interfaces.http.controllers.user_controllers import users_bp
from app.interfaces.http.controllers.user_controllers.factories.read_all_controller_factory import (
    read_all_factory,
)


@users_bp.route("/", methods=["GET"])
@login_required
def get_users():

    factory = read_all_factory()

    service = GetUsersService(factory["user_repository"])
    users = service.to_execute(factory["command"])

    return jsonify(users.to_list_of_dicts())
