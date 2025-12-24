from flask import Flask

from app.errors import register_error_handlers

from .routes import register_routes
from .config import Config
from .extensions import db, login_manager
from .models.reservation import Reservation
from .models.table import Table
from .models.user import User


def create_app():
    app = Flask(__name__)

    register_routes(app)
    register_error_handlers(app)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
