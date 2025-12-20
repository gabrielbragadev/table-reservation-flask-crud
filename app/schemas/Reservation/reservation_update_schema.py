from marshmallow import fields, Schema
from marshmallow.validate import Length


class ReservationUpdateSchema(Schema):
    client_name = fields.Str(
        validate=Length(
            min=1, error="Nome do Cliente não pode conter espaços em branco"
        )
    )
    table_number = fields.Integer(
        validate=Length(min=1, error="Número da mesa não pode conter espaços em branco")
    )
    booking_date = fields.Date(
        validate=Length(
            min=1, error="Data da reserva não pode conter espaços em branco"
        )
    )
    initial_time = fields.Time(
        validate=Length(min=1, error="Hora de ínicio não pode conter espaços em branco")
    )
    final_time = fields.Time(
        validate=Length(min=1, error="Hora de fim não pode conter espaços em branco")
    )
