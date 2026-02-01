from typing import Dict

from flask_login import current_user
from app.application.commands.table.create_table_command import CreateTableCommand
from app.application.dtos.table.create_table_dto import CreateTableDTO
from app.infrastructure.persistence.sqlalchemy.table_repository import TableRepository
from app.infrastructure.extensions import db
from app.infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository


def create_table_factory(data: Dict) -> Dict[object]:
    table_repository = TableRepository(db.session)
    user_repository = UserRepository(db.session)
    unit_of_work = SqlAlchemyUnitOfWork(db.session)

    requester = user_repository.find_by_id(current_user.id)

    dto = CreateTableDTO(data.get("table_number"), data.get("people_capacity"))
    command = CreateTableCommand(dto, requester.role, requester.id)

    return {
        "table_repository": table_repository,
        "unit_of_work": unit_of_work,
        "command": command,
    }
