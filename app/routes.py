from flask import current_app as app, request, jsonify
from app.services.create_user_service import CreateUser
from app.services.create_reservation_service import CreateReservation
from app.services.userLogin_service import UserLogin
from app.services.read_reservations_service import Get_reservations
from app.services.delete_reservation_service import Delete_reservation
from app.services.update_reservation_service import Update_reservation
from app.services.read_user_service import Get_users
from flask_login import login_required


def register_routes(app):
    @app.route("/login", methods=["POST"])
    def Login():
        data = request.get_json()
        current_login = UserLogin(data)
        return current_login

    @app.route("/users", methods=["POST"])
    @login_required
    def User_create():
        data = request.get_json()
        new_user = CreateUser(data)
        return new_user

    @app.route("/users", methods=["GET"])
    @login_required
    def User_read():
        read_users = Get_users()
        return read_users

    @app.route("/reservations/create", methods=["POST"])
    @login_required
    def Reservation_create():
        data = request.get_json()
        new_reservation = CreateReservation(data)
        return new_reservation

    @app.route("/reservations/", methods=["GET"])
    @login_required
    def Reservations_read():
        read_reservations = Get_reservations()
        return read_reservations

    @app.route("/reservations/cancellation/<int:id>", methods=["DELETE"])
    @login_required
    def Reservation_cancellation(id):
        delete_reservation = Delete_reservation(id)
        return delete_reservation

    @app.route("/reservations/edit/<int:id>", methods=["PUT"])
    @login_required
    def Reservation_edit(id):
        data = request.get_json()
        reservation_edit = Update_reservation(data, id)
        return reservation_edit
