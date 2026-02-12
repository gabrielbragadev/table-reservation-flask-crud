from flask import jsonify
from flask_login import current_user, login_required


from app.application.commands.user.read_user_command import ReadUserCommand
from app.application.dtos.user.read_user_dto import ReadUserDTO
from app.application.services.user.read_user_service import GetUserService
from app.infrastructure.extensions import db

from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository
from app.interfaces.http.controllers.user_controllers import users_bp


@users_bp.route("/<int:user_id>", methods=["GET"])
@login_required
def get_user(user_id):

    user_repository = UserRepository(db.session)
    requester = user_repository.find_by_id(current_user.id)

    command = ReadUserCommand(user_id, requester.role, requester.id)

    service = GetUserService(user_repository)
    response = service.to_execute(command)

    dto = ReadUserDTO(
        command.user_id, response["username"], response["email"], response["role"]
    )

    return jsonify(dto.to_dict()), 200
