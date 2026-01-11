from flask import jsonify, request
from app.exceptions import UnauthorizedError
from app.routes.auth_routes import auth_bp
from app.schemas.user.user_login_schema import UserLoginSchema
from app.services.auth.userLogin_service import user_login_service


@auth_bp.route("/login", methods=["POST"])
def login_user():
    data = UserLoginSchema().load(request.get_json())

    try:
        user_login_service(data)
        return jsonify({"message": "Login realizado com sucesso"}), 200
    except UnauthorizedError as error:
        return jsonify({"error": str(error.message)}), 403
