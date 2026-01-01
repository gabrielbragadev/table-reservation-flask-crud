import bcrypt
from flask import abort, jsonify
from flask_login import current_user

from app.extensions import db
from app.models.user import User


def create_user_service(data):
    username = data.get("username")
    password = str.encode(data.get("password"))
    email = data.get("email")
    role = data.get("role")

    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    registered_users = User.query.all()
    if not registered_users and current_user.is_authenticated == False:
        user = User(username=username, password=hashed, email=email, role=role)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso"}), 201

    if not current_user.is_authenticated:
        abort(401, description="Sessão inválida ou expirada. Faça login novamente.")

    authenticated_user = User.query.filter_by(id=current_user.id).first()

    if authenticated_user.role == "user":
        abort(403)

    user = User(username=username, password=hashed, email=email, role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuário cadastrado com sucesso"}), 201
