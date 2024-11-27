from App.database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from App.models.reviewCommand import ReviewCommand


class RatingCommand(ReviewCommand):
    __tablename__ = 'rating_command'

    id = Column(Integer, primary_key=True)
    review_id = Column(Integer, ForeignKey("review.id"), nullable=False)
    rating_value = Column(Integer, nullable=False)

    review = relationship("Review", back_populates="rating_commands")

    __mapper_args__ = {"polymorphic_identity": "rating_command"}

    def __init__(self, review_id: int, rating_value: int):
        super().__init__()
        self.review_id = review_id
        self.rating_value = rating_value

    def to_json(self):
        return {
            "id": self.id,
            "review_id": self.review_id,
            "rating_value": self.rating_value,
        }

    def __repr__(self):
        return f"<RatingCommand id={self.id}, review_id={self.review_id}, rating_value={self.rating_value}>"
