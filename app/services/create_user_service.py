from app.models.user import User
from app.extensions import db
from flask import jsonify


def CreateUser(data):
    if data.get("username") and data.get("password"):
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso"}), 201
    return jsonify({"message": "Os dados não foram totalmente preenchidos"}), 400
