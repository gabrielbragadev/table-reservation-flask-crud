from flask import abort, jsonify
from flask_login import current_user, logout_user


def user_logout_service():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({"message": "Logout realizado com sucesso"})
    abort(403)
