from app.interfaces.http.controllers.reservation_routes import reservations_bp
from app.interfaces.http.controllers.auth_routes import auth_bp
from app.interfaces.http.controllers.user_routes import users_bp


def register_routes(app):
    app.register_blueprint(reservations_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
