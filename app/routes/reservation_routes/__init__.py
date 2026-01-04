from flask import Blueprint

reservations_bp = Blueprint("reservations_bp", __name__, url_prefix="/reservations")


from app.routes.reservation_routes import create
