from flask import request, jsonify
from app.drivers.bcrypt_handler import BcryptHandler
from app.infrastructure.extensions import db

from app.domain.exceptions import ConflictError, ForbiddenError, UnauthorizedError
from app.application.services.user.create_user_service import CreateUserService
from app.interfaces.http.schemas.user.user_create_schema import UserCreateSchema
from app.interfaces.http.controllers.user_controllers import users_bp
from app.application.commands.user.create_user_command import CreateUserCommand
from app.drivers.flask_login_handler import FlaskLoginHandler
from app.application.dtos.user.create_user_dto import CreateUserDTO
from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository
from app.infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.extensions import db


@users_bp.route("/", methods=["POST"])
def create_user():

    data = UserCreateSchema().load(request.get_json())
    login_handler = FlaskLoginHandler()
    bcrypt_handler = BcryptHandler()
    user_repository = UserRepository(db.session)
    unit_of_work = SqlAlchemyUnitOfWork(db.session)

    current_user = user_repository.find_by_id(login_handler.find_current_user_id)

    dto = CreateUserDTO(
        username=data.get("username"),
        password=data.get("password"),
        email=data.get("email"),
        role=data.get("role"),
    )

    dto.encode_and_hashed_password(bcrypt_handler)

    command = CreateUserCommand(
        requester_role=("admin" if current_user is None else current_user.username),
        requester_user_id=(0 if current_user is None else current_user.id),
        data=dto,
    )

    try:
        service = CreateUserService(user_repository, login_handler, unit_of_work)
        service.to_execute(command)
        return jsonify({"message": "Usuário criado com sucesso"}), 201
    except UnauthorizedError as error:
        return jsonify({"error": error.message}), 401
    except ForbiddenError as error:
        return jsonify({"error": error.message}, 403)
    except ConflictError as error:
        return jsonify({"error": error.message}), 409
    except Exception as error:
        return jsonify({"error": str(error)}), 500
