from flask import jsonify
from app.extensions import db

from app.exceptions import (
    ForbiddenError,
    NotFoundError,
)
from app.services.user.delete_user_service import DeleteUserService
from app.routes.user_routes import users_bp


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def create_user(user_id: int):
    try:
        service = DeleteUserService(user_id, db.session)
        service.to_execute()
        return jsonify({"message": "Usuário excluído com sucesso"}), 200
    except ForbiddenError as error:
        return jsonify({"error": error.message}, 403)
    except NotFoundError as error:
        return jsonify({"error": error.message}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500
