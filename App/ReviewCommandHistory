from datetime import datetime
from App.database import db


class ReviewCommandHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewCommand_id = db.Column(db.Integer, db.ForeignKey('reviewCommand.id'), nullable=False)
    reviewCommand = db.relationship('ReviewCommand', backref='reviewCommandHistory', lazy=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, reviewCommand_id: int):
        self.reviewCommand_id = reviewCommand_id

    def __repr__(self):
        return f"<ReviewCommand History {self.reviewCommand_id} at {self.timestamp}>"
