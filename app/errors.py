from marshmallow import ValidationError


def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return {"message": "Erro de validação", "errors": err.messages}, 400
