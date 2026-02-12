from flask import Blueprint

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


from app.interfaces.http.controllers.auth_controllers import login
from app.interfaces.http.controllers.auth_controllers import logout
