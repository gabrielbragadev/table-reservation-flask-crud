from ..models.user import User
from flask import jsonify


def Get_users():
    users = User.query.all()
    response = [{"id": u.id, "username": u.username} for u in users]
    return jsonify(response)
