from app.extensions import db
from sqlalchemy.orm import relationship


class Table(db.Model):
    __tablename__ = "tables"

    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, unique=True, nullable=False)
    people_capacity = db.Column(db.Integer, nullable=False)

    reservations = db.relationship("Reservation", back_populates="table")
