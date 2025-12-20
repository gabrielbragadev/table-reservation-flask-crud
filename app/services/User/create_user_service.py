from app.models.user import User
from app.extensions import db
from flask import jsonify
from flask_login import current_user
import bcrypt


def CreateUser(data):
    username = data.get("username")
    password = str.encode(data.get("password"))
    email = data.get("email")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    registered_users = User.query.all()
    if not registered_users and current_user.is_authenticated == False:
        user = User(username=username, password=hashed, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso"}), 201

    if not current_user.is_authenticated:
        return (
            jsonify(
                {"messsage": "É preciso estar autenticado para realizar essa ação!"}
            )
        ), 401

    user = User(username=username, password=hashed, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuário cadastrado com sucesso"}), 201
