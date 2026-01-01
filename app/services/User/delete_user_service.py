from flask import abort, jsonify
from flask_login import current_user

from app.extensions import db
from app.models.user import User


def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    authenticated_user = User.query.filter_by(id=current_user.id).first()

    if current_user.id == user_id:
        abort(
            403,
            description="Você não pode excluir seu próprio usuário enquanto estiver logado",
        )

    if authenticated_user.role == "user":
        abort(403)

    if user is None:
        abort(404)

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Registro excluído com sucesso"})
