from flask import jsonify

from app.application.services.user.create_user_service import CreateUserService
from app.interfaces.http.controllers.user_controllers.factories.create_controller_factory import (
    create_controller_factory,
)
from app.interfaces.http.controllers.user_controllers import users_bp


@users_bp.route("/", methods=["POST"])
def create_user():

    factory = create_controller_factory()

    service = CreateUserService(
        factory["user_repository"],
        factory["login_handler"],
        factory["unit_of_work"],
    )

    service.to_execute(factory["command"])
    return jsonify({"message": "Usuário criado com sucesso"}), 201
