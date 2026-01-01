from flask import Flask, jsonify

from app.errors import register_error_handlers

from app.routes import register_routes
from app.config import Config
from app.extensions import db, login_manager, socketio
from app.models.reservation import Reservation
from app.models.table import Table
from app.models.user import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = None
    socketio.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return (
            jsonify(
                {
                    "error": "unauthorized",
                    "message": "Sessão inválida ou expirada. Faça login novamente.",
                }
            ),
            401,
        )

    register_routes(app)
    register_error_handlers(app)

    return app
