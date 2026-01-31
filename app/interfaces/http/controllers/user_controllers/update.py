from typing import Dict
from flask import request, jsonify
from app.application.services.user.update_user_service import UpdateUserService
from app.interfaces.http.controllers.user_controllers import users_bp
from flask_login import login_required
from app.interfaces.http.schemas.user.user_update_schema import UserUpdateSchema
from app.interfaces.http.controllers.user_controllers.factories.update_controller_factory import (
    update_controller_factory,
)


@users_bp.route("/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id: int) -> Dict:

    data = UserUpdateSchema().load(request.get_json())

    factory = update_controller_factory(user_id, data)

    service = UpdateUserService(
        factory["user_repository"], factory["bcrypt_handler"], factory["unit_of_work"]
    )
    response = service.to_execute(factory["command"])

    return (
        jsonify(
            {
                "message": "Alteração realizada com sucesso",
                "Dados pós alteração": {
                    "username": response.username,
                    "e-mail": response.email,
                    "role": response.role,
                },
            }
        ),
        200,
    )
