from app.exceptions import (
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)
from flask import jsonify
from marshmallow import ValidationError


def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return (
            jsonify(
                {
                    "error": "validation",
                    "message": "Erro de validação",
                    "errors": err.messages,
                }
            ),
            400,
        )

    @app.errorhandler(UnauthorizedError)
    def unauthorized_error(err):
        message = (
            (err.description)
            if hasattr(err, "description")
            else getattr(err, "message", "Não autorizado")
        )
        return jsonify({"error": "unauthorized", "message": message}), 401

    @app.errorhandler(ForbiddenError)
    def forbidden_error(err):
        message = (
            (err.description)
            if hasattr(err, "description")
            else getattr(err, "message", "Acesso Negado")
        )
        return jsonify({"error": "forbidden", "message": message}), 401

    @app.errorhandler(NotFoundError)
    def notfound_error(err):
        message = (
            (err.description)
            if hasattr(err, "description")
            else getattr(err, "message", "Não encontrado")
        )

        return (
            jsonify(
                {
                    "error": "not_found",
                    "message": message,
                }
            ),
            404,
        )

    @app.errorhandler(ConflictError)
    def conflict_error(err):
        message = (
            err.description
            if hasattr(err, "description")
            else getattr(err, "message", "Conflito")
        )
        return jsonify({"error": "conflict", "message": message}), 409

    @app.errorhandler(422)
    def unprocessable_content(err):
        return (
            jsonify(
                {
                    "error": "unprocessable_content",
                    "message": (
                        err.description
                        if hasattr(err, "description")
                        else "Falha na validação dos dados. Campos obrigatórios ausentes ou inválidos."
                    ),
                }
            ),
            422,
        )

    @app.errorhandler(500)
    def internal_error(err):
        return (
            jsonify({"error": "internal_error", "message": "Erro interno no servidor"}),
            500,
        )
