import bcrypt
from flask import abort, jsonify
from flask_login import current_user, login_user

from app.extensions import db
from app.models.user import User


def user_login_service(data):
    username = data.get("username")
    password = str.encode(data.get("password"))
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.checkpw(password, str.encode(user.password)):
        login_user(user)
        return jsonify({"message": "Autenticação Feita Com Sucesso"}), 200
    abort(401, description="Credenciais Inválidas")
