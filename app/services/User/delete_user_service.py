from flask import jsonify
from flask_login import current_user

from app.extensions import db
from app.models.user import User


def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    authenticated_user = User.query.filter_by(id=current_user.id).first()

    if current_user.id == user_id:
        return (
            jsonify(
                {
                    "message": "Você não pode excluir seu próprio usuário enquanto estiver logado"
                }
            ),
            401,
        )

    if authenticated_user.role == "user":
        return (jsonify({"messsage": "Usuário não autorizado"})), 401

    if user is None:
        return jsonify({"message": "Registro não encontrado"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Registro excluído com sucesso"})
