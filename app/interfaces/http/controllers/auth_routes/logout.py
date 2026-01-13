from flask import jsonify
from flask_login import login_required
from app.domains.exceptions import UnauthorizedError
from app.interfaces.http.controllers.auth_routes import auth_bp
from app.application.services.auth.logout_service import user_logout_service


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout_user():
    try:
        user_logout_service()
        return jsonify({"message": "Logout realizado com sucesso"}), 200
    except UnauthorizedError as error:
        return jsonify({"error": error.message})
