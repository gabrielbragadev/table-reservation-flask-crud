from flask import jsonify
from flask_login import login_required

from app.interfaces.http.controllers.user_controllers import users_bp
from app.application.services.user.request_delete_account_service import (
    RequestDeleteAccountService,
)
from app.interfaces.http.controllers.user_controllers.factories.request_account_delete_otp_factory import (
    generation_delete_acc_otp_factory,
)


@users_bp.route("/me/deletion-otp", methods=["POST"])
@login_required
def generation_delete_acc_otp():

    factory = generation_delete_acc_otp_factory()

    service = RequestDeleteAccountService(
        factory["unit_of_work"], factory["cryptocode_handler"]
    )
    response = service.request_account_delete_otp(factory["current_user"])
    return jsonify(response), 200
