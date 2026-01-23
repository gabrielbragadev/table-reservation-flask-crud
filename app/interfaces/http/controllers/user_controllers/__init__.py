from flask import Blueprint

users_bp = Blueprint("users_bp", __name__, url_prefix="/users")


from app.interfaces.http.controllers.user_controllers import create
from app.interfaces.http.controllers.user_controllers import delete
from app.interfaces.http.controllers.user_controllers import request_account_delete_otp
