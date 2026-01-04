from app.routes.reservation_routes import reservations_bp


def register_routes(app):
    app.register_blueprint(reservations_bp)
