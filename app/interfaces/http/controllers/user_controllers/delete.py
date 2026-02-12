from flask import jsonify
from flask_login import login_required
from app.application.services.user.delete_user_service import DeleteUserService
from app.interfaces.http.controllers.user_controllers import users_bp
from app.interfaces.http.controllers.user_controllers.factories.delete_controller_factory import (
    delete_controller_factory,
)


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id: int):

    factory = delete_controller_factory(user_id)

    service = DeleteUserService(
        factory["user_repository"],
        factory["login_handler"],
        factory["unit_of_work"],
        factory["cryptocode_handler"],
    )
    service.to_execute(factory["command"])
    return jsonify({"message": "Usuário excluído com sucesso"}), 200
