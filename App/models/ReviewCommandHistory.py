from datetime import datetime
from App.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class ReviewCommandHistory(Base):
    __tablename__ = 'review_command_history'

    id = Column(Integer, primary_key=True)
    review_command_id = Column(Integer, ForeignKey('review_command.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    review_command = relationship('ReviewCommand', back_populates='history')

    def __init__(self, review_command_id: int):
        self.review_command_id = review_command_id

    def to_json(self):
        return {
            "id": self.id,
            "review_command_id": self.review_command_id,
            "timestamp": self.timestamp.isoformat()
        }

    def __repr__(self):
        return f"<ReviewCommandHistory id={self.id}, command_id={self.review_command_id}, timestamp={self.timestamp}>"
