from flask import Blueprint

reservations_bp = Blueprint("reservations_bp", __name__, url_prefix="/reservations")


from app.interfaces.http.controllers.reservation_routes import create
from app.interfaces.http.controllers.reservation_routes import read
from app.interfaces.http.controllers.reservation_routes import read_all
from app.interfaces.http.controllers.reservation_routes import cancel
