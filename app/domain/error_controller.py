from flask import jsonify
from app.domain.exceptions import (
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)
import logging


def register_error_handlers(app):

    @app.errorhandler(ConflictError)
    @app.errorhandler(ForbiddenError)
    @app.errorhandler(NotFoundError)
    @app.errorhandler(UnauthorizedError)
    def handle_domain_errors(error):
        return (
            jsonify({"errors": [{"title": error.name, "detail": error.message}]}),
            error.status_code,
        )

    @app.errorhandler(Exception)
    def handle_generic_error(error):

        logging.error("Server Error", exc_info=True)

        return (
            jsonify({"errors": [{"title": "Server Error", "detail": str(error)}]}),
            500,
        )
