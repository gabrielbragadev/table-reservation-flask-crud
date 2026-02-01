from flask import Blueprint

tables_bp = Blueprint("tables_bp", __name__, url_prefix="/tables")


from app.interfaces.http.controllers.table_controllers import create
