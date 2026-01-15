from flask import Blueprint

reservations_bp = Blueprint("reservations_bp", __name__, url_prefix="/reservations")


from app.interfaces.http.controllers.reservation_controllers import create
from app.interfaces.http.controllers.reservation_controllers import read
from app.interfaces.http.controllers.reservation_controllers import read_all
from app.interfaces.http.controllers.reservation_controllers import cancel
