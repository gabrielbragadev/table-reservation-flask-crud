from app.interfaces.http.controllers.reservation_controllers import reservations_bp
from app.interfaces.http.controllers.auth_controllers import auth_bp
from app.interfaces.http.controllers.user_controllers import users_bp
from app.interfaces.http.controllers.table_controllers import tables_bp


def register_routes(app):
    app.register_blueprint(reservations_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(tables_bp)
