from typing import Dict
from flask_login import current_user

from app.application.commands.user.read_users_command import ReadUsersCommand
from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository
from app.infrastructure.extensions import db


def read_all_factory() -> dict:
    user_repository = UserRepository(db.session)

    requester = user_repository.find_by_id(current_user.id)

    command = ReadUsersCommand(
        requester_role=requester.role, requester_user_id=requester.id
    )

    return {"user_repository": user_repository, "command": command}
