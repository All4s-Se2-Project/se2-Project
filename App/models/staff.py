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
    
    #method for searching student
   def studentSearch(self, username, studentID, faculty, degree):
        return Student.query.filter_by(
            username=username, 
            ID=studentID, 
            faculty=faculty, 
            degree=degree
        ).first()
    
    #method for creating a review
    def createReview(self, reviewType, studentName, teacher, studentID, topic, details, points):
        review = Review(
            reviewType=reviewType,
            studentName=studentName,
            teacher=teacher,
            studentID=studentID,
            topic=topic,
            details=details,
            points=points,
            staffID=self.ID
        )
        db.session.add(review)
        db.session.commit()
        return review

    #method to add rating
    def addRating(self, ReviewID, rating):
        review = Review.query.get(ReviewID)
        if review:
            review.rating = rating
            db.session.commit()
            return review.rating
        raise ValueError("Review not found.")

    #method to delete review
    def deleteReview(self, ReviewID):
        review = Review.query.get(ReviewID)
        
        if review:
            db.session.delete(review)
            db.session.commit()

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
