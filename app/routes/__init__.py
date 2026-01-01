from .auth_routes import register_auth_routes
from .user_routes import register_user_routes
from .reservation_routes import register_reservation_routes
from .table_routes import register_table_routes
from .socket_routes import register_socket_routes


def register_routes(app):
    register_auth_routes(app)
    register_user_routes(app)
    register_reservation_routes(app)
    register_table_routes(app)
    register_socket_routes()
