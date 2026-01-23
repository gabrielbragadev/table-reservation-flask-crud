from typing import Dict

from flask import request
from app.application.commands.auth.user_login_command import UserLoginCommand
from app.application.dtos.auth.user_login_dto import UserLoginDTO
from app.drivers.flask_login_handler import FlaskLoginHandler
from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository
from app.drivers.bcrypt_handler import BcryptHandler
from app.infrastructure.extensions import db
from app.interfaces.http.schemas.user.user_login_schema import UserLoginSchema


def login_controller_factory() -> Dict[object]:
    bcrypt_handler = BcryptHandler()
    user_repository = UserRepository(db.session)
    flask_login_handler = FlaskLoginHandler()

    data = UserLoginSchema().load(request.get_json())

    dto = UserLoginDTO(data["username"], data["password"])
    dto.to_bytes()

    command = UserLoginCommand(dto)

    return {
        "bcrypt_handler": bcrypt_handler,
        "user_repository": user_repository,
        "flask_login_handler": flask_login_handler,
        "data": data,
        "dto": dto,
        "command": command,
        "request": request
    }
