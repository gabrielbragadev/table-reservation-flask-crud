from flask import jsonify
from flask_login import login_required
from app.infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork
from app.drivers.flask_login_handler import FlaskLoginHandler

from app.infrastructure.extensions import db
from app.interfaces.http.controllers.user_controllers import users_bp
from app.infrastructure.persistence.sqlalchemy.user_repository import UserRepository
from app.application.services.user.request_delete_account_service import (
    RequestDeleteAccountService,
)


@users_bp.route("/me/deletion-otp", methods=["POST"])
@login_required
def generation_delete_acc_otp():

    user_repository = UserRepository(db.session)
    login_handler = FlaskLoginHandler()
    unit_of_work = SqlAlchemyUnitOfWork(db.session)

    current_user = user_repository.find_by_id(login_handler.find_current_user_id())

    try:
        service = RequestDeleteAccountService(unit_of_work)
        response = service.request_account_delete_otp(current_user)
        return jsonify(response), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 500
