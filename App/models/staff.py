#removed reports and pending accomplishments 
#added new methods

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey
from App.models.user import User


class Staff(User):
    __tablename__ = 'staff'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    reviews = relationship('Review', backref='staffReviews', lazy='joined')
    __mapper_args__ = {"polymorphic_identity": "staff"}

    def __init__(self, username, first_name, last_name, email, password, faculty):
        super().__init__(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            faculty=faculty
        )
        
    def to_json(self) -> dict:
        return {
            "staffID": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "faculty": self.faculty,
            "reviews": [review.to_json() for review in self.reviews]
        }

    def __repr__(self):
        return f'<Staff {self.id}: {self.email}>'
 