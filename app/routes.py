from flask import request
from flask_login import login_required

from app.schemas.Reservation.reservation_create_schema import ReservationCreateSchema
from app.schemas.Reservation.reservation_update_schema import ReservationUpdateSchema
from app.schemas.Table.create_table_schema import CreateTableSchema
from app.schemas.Table.update_table_schema import UpdateTableSchema
from app.schemas.User.user_create_schema import UserCreateSchema
from app.schemas.User.user_login_schema import UserLoginSchema
from app.services.Auth.logout_service import user_logout_service
from app.services.Auth.userLogin_service import user_login_service
from app.services.Reservation.create_reservation_service import (
    create_reservation_service,
)
from app.services.Reservation.delete_reservation_service import (
    delete_reservation_service,
)
from app.services.Reservation.read_reservations_service import get_reservations_service
from app.services.Reservation.read_reservation_service import get_reservation_service
from app.services.Reservation.update_reservation_service import (
    update_reservation_service,
)
from app.services.Table.create_table_service import create_table_service
from app.services.Table.read_tables_service import get_tables_service
from app.services.Table.read_table_service import get_table_service
from app.services.Table.delete_table_service import delete_table_service
from app.services.Table.update_table_service import update_table
from app.services.User.create_user_service import create_user_service
from app.services.User.read_users_service import get_users_service
from app.services.User.delete_user_service import delete_user


def register_routes(app):
    @app.route("/login", methods=["POST"])
    def login():
        data = UserLoginSchema().load(request.get_json())
        current_login = user_login_service(data)
        return current_login

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        logout = user_logout_service()
        return logout

    @app.route("/users", methods=["POST"])
    def user_create():
        data = UserCreateSchema().load(request.get_json())
        new_user = create_user_service(data)
        return new_user

    @app.route("/users", methods=["GET"])
    @login_required
    def user_read():
        read_users = get_users_service()
        return read_users
    
    @app.route("/users/delete/<int:user_id>", methods=["DELETE"])
    @login_required
    def user_delete(user_id):
        user_delete = delete_user(user_id)
        return user_delete

    @app.route("/reservations/create", methods=["POST"])
    @login_required
    def reservation_create():
        data = ReservationCreateSchema().load(request.get_json())
        new_reservation = create_reservation_service(data)
        return new_reservation

    @app.route("/reservations/", methods=["GET"])
    @login_required
    def reservations_read():
        read_reservations = get_reservations_service()
        return read_reservations

    @app.route("/reservations/<int:reservation_id>", methods=["GET"])
    @login_required
    def reservation_read(reservation_id):
        read_reservation = get_reservation_service(reservation_id)
        return read_reservation

    @app.route("/reservations/cancellation/<int:reservation_id>", methods=["DELETE"])
    @login_required
    def reservation_cancellation(reservation_id):
        delete_reservation = delete_reservation_service(reservation_id)
        return delete_reservation

    @app.route("/reservations/edit/<int:reservation_id>", methods=["PUT"])
    @login_required
    def reservation_edit(reservation_id):
        data = ReservationUpdateSchema().load(request.get_json())
        reservation_edit = update_reservation_service(data, reservation_id)
        return reservation_edit

    @app.route("/tables/create", methods=["POST"])
    @login_required
    def table_create():
        data = CreateTableSchema().load(request.get_json())
        table_create = create_table_service(data)
        return table_create

    @app.route("/tables", methods=["GET"])
    @login_required
    def tables_read():
        tables_read = get_tables_service()
        return tables_read

    @app.route("/tables/<int:table_id>", methods=["GET"])
    @login_required
    def table_read(table_id):
        table_read = get_table_service(table_id)
        return table_read

    @app.route("/tables/delete/<int:table_id>", methods=["DELETE"])
    @login_required
    def table_delete(table_id):
        table_delete = delete_table_service(table_id)
        return table_delete

    @app.route("/tables/edit/<int:table_id>", methods=["PUT"])
    @login_required
    def table_update(table_id):
        data = UpdateTableSchema().load(request.get_json())
        table_update = update_table(data, table_id)
        return table_update
