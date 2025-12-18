from app.models.user import User
from app.extensions import db
from flask import jsonify
import bcrypt


def CreateUser(data):
    username = data.get("username")
    password = str.encode(data.get("password"))
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    if username and hashed:
        user = User(username=username, password=hashed)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso"}), 201
    return jsonify({"message": "Os dados não foram totalmente preenchidos"}), 400
