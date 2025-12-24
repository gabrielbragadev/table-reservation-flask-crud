from sqlalchemy.orm import relationship

from app.extensions import db


class Table(db.Model):
    __tablename__ = "tables"

    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, unique=True, nullable=False)
    people_capacity = db.Column(db.Integer, nullable=False)

    reservations = db.relationship("Reservation", back_populates="table")

    def to_dict(self):
        return {
            "id": self.id,
            "table_number": self.table_number,
            "people_capacity": self.people_capacity,
        }
