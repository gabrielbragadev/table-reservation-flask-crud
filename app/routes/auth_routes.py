from flask import request, jsonify
from flask_login import login_required

from app.schemas.User.user_login_schema import UserLoginSchema
from app.services.Auth.userLogin_service import user_login_service
from app.services.Auth.logout_service import user_logout_service


def register_auth_routes(app):
    @app.route("/auth/login", methods=["POST"])
    def login():
        data = UserLoginSchema().load(request.get_json())
        current_login = user_login_service(data)
        return current_login

    @app.route("/auth/logout", methods=["POST"])
    @login_required
    def logout():
        logout = user_logout_service()
        return logout

