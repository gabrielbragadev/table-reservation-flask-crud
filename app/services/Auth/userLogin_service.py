from app.drivers.bcrypt_handler import BcryptHandler
from flask import abort, jsonify
from flask_login import current_user, login_user

from app.extensions import db
from app.models.user import User


def user_login_service(data):
    bcrypt_handler = BcryptHandler()

    username = data.get("username")
    password = str.encode(data.get("password"))
    user = User.query.filter_by(username=username).first()
    if user and bcrypt_handler.verify_password(user, password):
        login_user(user)
        return jsonify({"message": "Autenticação Feita Com Sucesso"}), 200
    abort(401, description="Credenciais Inválidas")
