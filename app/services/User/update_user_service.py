import bcrypt

from flask import abort, jsonify
from flask_login import current_user

from app.exceptions import ConflictError
from app.extensions import db
from app.models.user import User


def update_user(data, user_id):

    username = data.get("username")
    user_identical_usernames = User.query.filter_by(username=username).first()

    password = str.encode(data.get("password"))

    email = data.get("email")
    user_identical_emails = User.query.filter_by(email=email).first()

    role = data.get("role")

    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    authenticated_user = User.query.filter_by(id=current_user.id).first()

    user_to_be_changed = User.query.filter_by(id=user_id).first()

    if authenticated_user.role == "user":
        if user_id != current_user.id:
            abort(403)

    if user_identical_usernames:
        raise ConflictError("Nome de usuário já existe")

    if user_identical_emails:
        raise ConflictError("E-mail já existe")

        if username:
            authenticated_user.username = username
        if password:
            authenticated_user.password = hashed
        if email:
            authenticated_user.email = email

        db.session.commit()

        return jsonify({"message": "Registro alterado com sucesso"})

    if user_to_be_changed is None:
        abort(404)

    if username:
        user_to_be_changed.username = username
    if password:
        user_to_be_changed.password = hashed
    if email:
        user_to_be_changed.email = email
    if role:
        user_to_be_changed.role = role

    db.session.commit()

    return jsonify({"message": "Registro alterado com sucesso"})
