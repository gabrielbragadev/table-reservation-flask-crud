from typing import Dict
from app.drivers.cryptocode_handler import CryptocodeHandler
from app.drivers.flask_login_handler import FlaskLoginHandler
from app.infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository
from app.infrastructure.extensions import db


def generation_delete_acc_otp_factory() -> dict:
    user_repository = UserRepository(db.session)
    login_handler = FlaskLoginHandler()
    unit_of_work = SqlAlchemyUnitOfWork(db.session)
    cryptocode_handler = CryptocodeHandler()

    current_user = user_repository.find_by_id(login_handler.find_current_user_id())

    return {
        "unit_of_work": unit_of_work,
        "cryptocode_handler": cryptocode_handler,
        "current_user": current_user,
    }
