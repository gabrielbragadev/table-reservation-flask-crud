from flask import jsonify
from app.domain.exceptions import NotFoundError, UnauthorizedError
from app.interfaces.http.controllers.auth_controllers import auth_bp

from app.application.services.auth.login_service import UserLoginService
from app.interfaces.http.controllers.auth_controllers.factories.login_controller_factory import (
    login_controller_factory,
)


@auth_bp.route("/login", methods=["POST"])
def login_user():
    factory = login_controller_factory()

    service = UserLoginService(
        factory["bcrypt_handler"],
        factory["user_repository"],
        factory["flask_login_handler"],
    )
    service.user_login(factory["command"], factory["request"])
    return jsonify({"message": "Login realizado com sucesso"}), 200
