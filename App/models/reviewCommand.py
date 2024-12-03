from datetime import datetime
from App.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from App.models import db


class ReviewCommand(db.Model):  
    __tablename__ = 'review_command'

    id = Column(Integer, primary_key=True)
    review_id = Column(Integer, ForeignKey('review.id'), nullable=False)
    command_type = Column(String(50), nullable=False)  
    executed_at = Column(DateTime, default=datetime.utcnow)

   
    history = relationship("ReviewCommandHistory", back_populates="review_command")
    review = relationship("Review", back_populates="commands", overlaps="rating_commands")

    def __init__(self, review_id: int, command_type: str):
        self.review_id = review_id
        self.command_type = command_type

    def execute(self):
        """Default execute behavior with logging"""
        if self.command_type == "mark_helpful":
            print(f"Marking Review ID {self.review_id} as helpful.")
        elif self.command_type == "flag_review":
            print(f"Flagging Review ID {self.review_id} for further inspection.")
        else:
            print(f"Executing default behavior for ReviewCommand ID {self.id}, Type {self.command_type}, at {datetime.utcnow()}.")

    def undo(self):
        """Default undo behavior with logging"""
        print(f"Undoing ReviewCommand ID {self.id}, Type {self.command_type}, at {datetime.utcnow()}.")

    def to_json(self):
        return {
            "id": self.id,
            "review_id": self.review_id,
            "command_type": self.command_type,
            "executed_at": self.executed_at.isoformat(),
        }

    def __repr__(self):
        return f"<ReviewCommand id={self.id}, type={self.command_type}, review_id={self.review_id}>"
