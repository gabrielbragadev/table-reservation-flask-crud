from flask import abort, jsonify
from flask_login import current_user

from ...models.user import User


def get_users_service():
    authenticated_user = User.query.filter_by(id=current_user.id).first()

    if authenticated_user.role == "user":
        abort(403)

    users = User.query.all()

    if users is None:
        abort(404)

    response = [
        {"id": u.id, "username": u.username, "email": u.email, "role": u.role}
        for u in users
    ]
    return jsonify(response)
