from marshmallow import Schema, fields, validate
from marshmallow.validate import Length


class UserUpdateSchema(Schema):
    username = fields.Str(
        validate=Length(min=1, error="Mínimo de caracteres é 1"),
        error_messages={"null": "Nome de usuário não pode ser nulo"},
    )

    email = fields.Email(
        validate=Length(min=6, error="Mínimo de caracteres é 6"),
        error_messages={
            "null": "E-mail não pode ser nulo",
        },
    )
    password = fields.Str(
        validate=Length(min=8, error="Mínimo de caracteres é 8"),
        error_messages={
            "null": "Senha não pode ser nula",
        },
    )
    role = fields.Str(
        validate=validate.OneOf(
            ["admin", "user"], error="O Cargo deve ser admin ou user"
        ),
        error_messages={
            "null": "Cargo não pode ser null",
        },
    )
