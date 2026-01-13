from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validate,
    validates_schema,
)

MESA_COM_MAIOR_CAPACIDADE = 6


class UpdateTableSchema(Schema):
    table_number = fields.Integer(
        error_messages={"null": "Número da mesa não pode ser null"}
    )
    people_capacity = fields.Integer(
        validate=validate.Range(
            min=1,
            max=MESA_COM_MAIOR_CAPACIDADE,
            error=f"Capacidade da mesa deve ser entre 1 e {MESA_COM_MAIOR_CAPACIDADE}",
        ),
        error_messages={"null": "Capacidade da mesa não pode ser null"},
    )

    @validates_schema
    def validate_table_rules(self, data, **kwargs):
        table_number = data.get("table_number")

        if table_number is not None:
            if table_number < 1:
                raise ValidationError(
                    "Número da mesa não pode ser menor que 1", field_name="table_number")