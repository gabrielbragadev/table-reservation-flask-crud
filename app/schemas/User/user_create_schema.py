from marshmallow import Schema, fields, validate
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
    role = fields.Str(
        required=True,
        validate=validate.OneOf(
            ["admin", "user"], error="O Cargo deve ser admin ou user"
        ),
        error_messages={
            "required": "Cargo é obrigatória",
            "null": "Cargo não pode ser nula",
        },
    )
