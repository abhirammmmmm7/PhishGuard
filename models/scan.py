from extensions import db
from datetime import datetime


class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    url = db.Column(db.String(500), nullable=False)
    prediction = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('scans', lazy=True))
