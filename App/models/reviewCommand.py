from datetime import datetime
from App.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from App.models import db


class ReviewCommand(db.Model): #change Base to db.Model
    __tablename__ = 'review_command'

    id = Column(Integer, primary_key=True)
    review_id = Column(Integer, ForeignKey('review.id'), nullable=False)
    command_type = Column(String(50), nullable=False)  # To identify the command type
    executed_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    history = relationship("ReviewCommandHistory", back_populates="review_command")
    review= relationship("Review", back_populates= "commands")

    def __init__(self, review_id: int, command_type: str):
        self.review_id = review_id
        self.command_type = command_type

    def execute(self):
        """Override this in specific command implementations"""
        raise NotImplementedError("Execute method must be implemented by subclasses.")

    def undo(self):
        """Override this in specific command implementations"""
        raise NotImplementedError("Undo method must be implemented by subclasses.")

    def to_json(self):
        return {
            "id": self.id,
            "review_id": self.review_id,
            "command_type": self.command_type,
            "executed_at": self.executed_at.isoformat(),
        }

    def __repr__(self):
        return f"<ReviewCommand id={self.id}, type={self.command_type}, review_id={self.review_id}>"
