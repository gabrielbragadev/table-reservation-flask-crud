from flask import jsonify

from ...models.user import User


def get_users_service():
    users = User.query.all()
    response = [{"id": u.id, "username": u.username, "email": u.email} for u in users]
    return jsonify(response)
