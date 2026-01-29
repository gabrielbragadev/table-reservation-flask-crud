from flask import jsonify, request
from flask_login import login_required
from app.infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork
from app.drivers.flask_login_handler import FlaskLoginHandler
from app.infrastructure.extensions import db
from app.application.services.user.delete_user_service import DeleteUserService
from app.interfaces.http.controllers.user_controllers import users_bp
from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository
from app.application.commands.user.delete_user_command import DeleteUserCommand
from app.interfaces.http.controllers.user_controllers.factories.delete_controller_factory import (
    delete_controller_factory,
)


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id: int):

    factory = delete_controller_factory(user_id)

    service = DeleteUserService(
        factory["user_repository"], factory["login_handler"], factory["unit_of_work"]
    )
    service.to_execute(factory["command"])
    return jsonify({"message": "Usuário excluído com sucesso"}), 200
