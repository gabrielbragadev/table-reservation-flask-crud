from flask import jsonify
from flask_login import login_required
from app.domain.exceptions import UnauthorizedError
from app.interfaces.http.controllers.auth_controllers import auth_bp
from app.application.services.auth.logout_service import LogoutService
from app.drivers.flask_login_handler import FlaskLoginHandler


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout_user():
    try:
        flask_login_handler = FlaskLoginHandler()
        service = LogoutService(flask_login_handler)
        service.user_logout_service()

        return jsonify({"message": "Logout realizado com sucesso"}), 200
    except UnauthorizedError as error:
        return jsonify({"error": error.message})
