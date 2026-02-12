from typing import Dict
from flask_login import current_user

from app.application.commands.user.update_user_command import UpdateUserCommand
from app.application.dtos.user.update_user_dto import UpdateUserDTO
from app.drivers.bcrypt_handler import BcryptHandler
from app.infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository
from app.infrastructure.extensions import db


def update_controller_factory(user_id: int, data: Dict) -> dict:
    user_repository = UserRepository(db.session)
    bcrypt_handler = BcryptHandler()
    unit_of_work = SqlAlchemyUnitOfWork(db.session)

    requester = user_repository.find_by_id(current_user.id)

    dto = UpdateUserDTO(
        data.get("username"),
        str.encode(data.get("password")),
        data.get("email"),
        data.get("role"),
    )

    command = UpdateUserCommand(user_id, dto, requester.id, requester.role)

    return {
        "user_repository": user_repository,
        "bcrypt_handler": bcrypt_handler,
        "unit_of_work": unit_of_work,
        "command": command,
    }
