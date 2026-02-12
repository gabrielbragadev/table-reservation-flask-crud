from flask import request

from app.application.commands.user.create_user_command import CreateUserCommand
from app.application.dtos.user.create_user_dto import CreateUserDTO
from app.drivers.bcrypt_handler import BcryptHandler
from app.drivers.flask_login_handler import FlaskLoginHandler
from app.infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository
from app.interfaces.http.schemas.user.user_create_schema import UserCreateSchema
from app.infrastructure.extensions import db


def create_controller_factory():

    data = UserCreateSchema().load(request.get_json())
    login_handler = FlaskLoginHandler()
    bcrypt_handler = BcryptHandler()
    user_repository = UserRepository(db.session)
    unit_of_work = SqlAlchemyUnitOfWork(db.session)

    current_user = user_repository.find_by_id(login_handler.find_current_user_id())

    dto = CreateUserDTO(
        username=data.get("username"),
        password=data.get("password"),
        email=data.get("email"),
        role=data.get("role"),
    )

    dto.encode_and_hashed_password(bcrypt_handler)

    command = CreateUserCommand(
        requester_role=("admin" if current_user is None else current_user.role),
        requester_user_id=(0 if current_user is None else current_user.id),
        data=dto,
    )

    return {
        "user_repository": user_repository,
        "login_handler": login_handler,
        "unit_of_work": unit_of_work,
        "command": command,
    }
