from marshmallow import fields, Schema, validate
from marshmallow.validate import Length


class ReservationUpdateSchema(Schema):
    client_name = fields.Str(
        validate=Length(
            min=1, error="Nome do Cliente não pode conter espaços em branco"
        )
    )
    people_quantity = fields.Integer()
    table_number = fields.Integer()
    booking_date = fields.Date()
    initial_time = fields.Time()
    final_time = fields.Time()
