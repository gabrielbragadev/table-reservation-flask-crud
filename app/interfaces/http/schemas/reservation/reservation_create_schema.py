from marshmallow import Schema, ValidationError, fields, validate, validates_schema
from marshmallow.validate import Length


class ReservationCreateSchema(Schema):
    id = fields.Integer(dump_only=True)
    client_name = fields.Str(
        required=True,
        validate=Length(
            min=1, error="Nome do Cliente não pode conter espaços em branco"
        ),
        error_messages={
            "required": "Nome é obrigatório",
            "null": "Nome não pode ser null",
        },
    )
    people_quantity = fields.Integer(
        required=True,
        validate=validate.Range(
            min=1, max=6, error="Não há mesas para essa quantidade de pessoas"
        ),
        error_messages={
            "required": "Quantidade de pessoas é obrigatória",
            "null": "Quantidade de pessoas não pode ser null",
        },
    )
    table_number = fields.Integer(
        required=True,
        error_messages={
            "required": "Número da mesa é obrigatório",
            "null": "Número da mesa não pode ser null",
        },
    )
    booking_date = fields.Date(
        required=True,
        error_messages={
            "required": "Data é obrigatória",
            "invalid": "Data deve estar no formato YYYY-MM-DD",
            "null": "Data não pode ser nula",
        },
    )
    initial_time = fields.Time(
        required=True,
        error_messages={
            "required": "Horário inicial é obrigatório",
            "invalid": "Horário inicial deve estar no formato HH:MM",
            "null": "Horário inicial não pode ser nulo",
        },
    )
    final_time = fields.Time(
        required=True,
        error_messages={
            "required": "Horário final é obrigatório",
            "invalid": "Horário final deve estar no formato HH:MM",
            "null": "Horário final não pode ser nulo",
        },
    )

    status = fields.Str(error_messages={"ivalid": "Status é string"})

    @validates_schema
    def validate_times(self, data, **kwargs):
        if data["final_time"] <= data["initial_time"]:
            raise ValidationError(
                "Hora de ínicio não pode ser maior que a hora de fim",
                field_name="initial_time",
            )
