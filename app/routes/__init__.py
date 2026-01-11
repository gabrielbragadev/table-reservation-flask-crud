from app.routes.reservation_routes import reservations_bp
from app.routes.auth_routes import auth_bp
from app.routes.user_routes import users_bp


def register_routes(app):
    app.register_blueprint(reservations_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
