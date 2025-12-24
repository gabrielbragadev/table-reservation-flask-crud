from marshmallow import Schema, ValidationError, fields, validate, validates_schema

MESA_COM_MAIOR_CAPACIDADE = 6


class CreateTableSchema(Schema):
    id = fields.Integer(dump_only=True)
    table_number = fields.Integer(
        required=True,
        error_messages={
            "required": "Número da mesa é obrigatório",
            "null": "Número da mesa não pode ser null",
        },
    )
    people_capacity = fields.Integer(
        required=True,
        validate=validate.Range(
            min=1,
            max=MESA_COM_MAIOR_CAPACIDADE,
            error="Capacidade da mesa ultrapassa quantidade máxima que é 6",
        ),
    )

    @validates_schema
    def validate_table_number(self, data, **kwargs):
        if data["table_number"] < 1:
            raise ValidationError(
                "Número da mesa não pode ser menor que 1", field_name="table_number"
            )
