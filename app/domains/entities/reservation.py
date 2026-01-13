from app.infrastructure.extensions import db


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(80), nullable=False)
    people_quantity = db.Column(db.Integer, nullable=False)
    table_number = db.Column(
        db.Integer, db.ForeignKey("tables.table_number"), nullable=False
    )
    booking_date = db.Column(db.Date, nullable=False)
    initial_time = db.Column(db.Time, nullable=False)
    final_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(80))

    table = db.relationship("Table", back_populates="reservations")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "client_name": self.client_name,
            "people_quantity": self.people_quantity,
            "table_number": self.table_number,
            "booking_date": self.booking_date,
            "initial_time": self.initial_time.isoformat(),
            "final_time": self.final_time.isoformat(),
            "table": {
                "table_number": self.table.table_number,
                "status": self.table.status,
            },
        }
