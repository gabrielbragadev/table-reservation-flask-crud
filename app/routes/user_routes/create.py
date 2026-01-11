from flask import request, jsonify

from app.exceptions import ConflictError, ForbiddenError, UnauthorizedError
from app.services.user.create_user_service import CreateUserService
from app.schemas.user.user_create_schema import UserCreateSchema
from app.routes.user_routes import users_bp


@users_bp.route("/", methods=["POST"])
def create_user():

    data = UserCreateSchema().load(request.get_json())

    try:
        service = CreateUserService(data)
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
