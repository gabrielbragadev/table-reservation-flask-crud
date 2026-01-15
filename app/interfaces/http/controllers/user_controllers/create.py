from flask import request, jsonify
from app.infrastructure.extensions import db

from app.domain.exceptions import ConflictError, ForbiddenError, UnauthorizedError
from app.application.services.user.create_user_service import CreateUserService
from app.interfaces.http.schemas.user.user_create_schema import UserCreateSchema
from app.interfaces.http.controllers.user_controllers import users_bp


@users_bp.route("/", methods=["POST"])
def create_user():

    data = UserCreateSchema().load(request.get_json())

    try:
        service = CreateUserService(data, db.session)
        service.create_user()
        return jsonify({"message": "Usuário criado com sucesso"}), 201
    except UnauthorizedError as error:
        return jsonify({"error": error.message}), 401
    except ForbiddenError as error:
        return jsonify({"error": error.message}, 403)
    except ConflictError as error:
        return jsonify({"error": error.message}), 409
    except Exception as error:
        return jsonify({"error": str(error)}), 500
