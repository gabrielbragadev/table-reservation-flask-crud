from marshmallow import Schema, fields
from marshmallow.validate import Length


class UserCreateSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str(
        required=True,
        validate=Length(min=1, error="Mínimo de caracteres é 1"),
        error_messages={
            "required": "Nome de usuário é obrigatório",
            "null": "Nome de usuário não pode ser nulo",
        },
    )
    email = fields.Email(
        required=True,
        validate=Length(min=6, error="Mínimo de caracteres é 6"),
        error_messages={
            "required": "E-mail é obrigatório",
            "null": "E-mail não pode ser nulo",
        },
    )
    password = fields.Str(
        required=True,
        validate=Length(min=8, error="Mínimo de caracteres é 8"),
        error_messages={
            "required": "Senha é obrigatória",
            "null": "Senha não pode ser nula",
        },
    )
