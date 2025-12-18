from app.models.user import User
from app.extensions import db
from flask import jsonify
from flask_login import login_user, current_user


def UserLogin(data):
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Autenticação Feita Com Sucesso"}), 200
        return jsonify({"message": "Credenciais Inválidas"}), 401
