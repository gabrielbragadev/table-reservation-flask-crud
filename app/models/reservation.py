
from app.extensions import db


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(80), nullable=False)
    table_number = db.Column(db.Integer, nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    initial_time = db.Column(db.Time, nullable=False)
    final_time = db.Column(db.Time, nullable=False)
