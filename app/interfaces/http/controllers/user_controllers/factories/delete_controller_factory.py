from typing import Dict
from flask import request

from app.application.commands.user.delete_user_command import DeleteUserCommand
from app.drivers.flask_login_handler import FlaskLoginHandler
from app.infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository
from app.infrastructure.extensions import db


def delete_controller_factory(user_id: int) -> Dict[object]:
    data = request.get_json(silent=True) or {}

    user_repository = UserRepository(db.session)
    login_handler = FlaskLoginHandler()
    unit_of_work = SqlAlchemyUnitOfWork(db.session)

    current_user = user_repository.find_by_id(login_handler.find_current_user_id())

    command = DeleteUserCommand(
        user_id=user_id,
        requester_user_id=current_user.id,
        requester_role=current_user.role,
        otp_code=data.get("otp_code"),
    )

    return {
        "user_repository": user_repository,
        "login_handler": login_handler,
        "unit_of_work": unit_of_work,
        "command": command,
    }
