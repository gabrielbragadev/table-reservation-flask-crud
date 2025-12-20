from flask import current_app as app, request, jsonify
from app.services.User.create_user_service import CreateUser
from app.services.Reservation.create_reservation_service import CreateReservation
from app.services.Auth.userLogin_service import UserLogin
from app.services.Reservation.read_reservations_service import Get_reservations
from app.services.Reservation.delete_reservation_service import Delete_reservation
from app.services.Reservation.update_reservation_service import Update_reservation
from app.services.User.read_user_service import Get_users
from app.services.Auth.logout_service import User_logout
from app.schemas.User.user_create_schema import UserCreateSchema
from app.schemas.User.user_login_schema import UserLoginSchema
from app.schemas.Reservation.reservation_create_schema import ReservationCreateSchema
from app.schemas.Reservation.reservation_update_schema import ReservationUpdateSchema
from flask_login import login_required


def register_routes(app):
    @app.route("/login", methods=["POST"])
    def Login():
        data = UserLoginSchema().load(request.get_json())
        current_login = UserLogin(data)
        return current_login

    @app.route("/logout", methods=["POST"])
    @login_required
    def Logout():
        logout = User_logout()
        return logout

    @app.route("/users", methods=["POST"])
    def User_create():
        data = UserCreateSchema().load(request.get_json())
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
        data = ReservationCreateSchema().load(request.get_json())
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
        data = ReservationUpdateSchema().load(request.get_json())
        reservation_edit = Update_reservation(data, id)
        return reservation_edit
