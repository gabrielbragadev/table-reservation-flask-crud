from app.infrastructure.extensions import socketio


def register_socket_routes():
    @socketio.on("connect")
    def handle_connect():
        print("Client connected to the server")
