from marshmallow import Schema, fields
from marshmallow.validate import Length


class UserLoginSchema(Schema):
    username = fields.Str(
        required=True,
        validate=Length(min=1, error="Username não pode conter espaços em branco"),
        error_messages={
            "required": "Nome de usuário é obrigatório",
            "null": "Nome de usuário não pode ser nulo",
        },
    )
    password = fields.Str(
        required=True,
        error_messages={
            "required": "Senha é obrigatória",
            "null": "Senha não pode ser nula",
        },
    )
