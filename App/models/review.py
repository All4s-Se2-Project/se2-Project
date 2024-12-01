from App.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, DateTime
from datetime import datetime
from App.database import db


class Review(db.Model):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.ID'), nullable=False)
    created_by_staff_id = Column(Integer, ForeignKey('staff.id'), nullable=False)
    is_positive = Column(Boolean, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    points = Column(Integer, nullable=False)
    details = Column(String(400), nullable=False)
    rating = Column(Integer, nullable=False)

    student = relationship('Student', backref='reviews', lazy=True)
    rating_commands = relationship("RatingCommand", back_populates="review")
    commands = relationship("ReviewCommand", back_populates="review", overlaps='rating_commands')
    
    def __init__(self, staff, student, is_positive, rating, points, details):
        self.created_by_staff_id = staff.id
        self.student_id = student.ID
        self.is_positive = is_positive
        self.points = points
        self.details = details
        self.date_created = datetime.utcnow()
        self.rating = rating

    def get_id(self):
        return self.id

    def to_json(self):
        return {
            "reviewID": self.id,
            "reviewer": f"{self.staff.firstname} {self.staff.lastname}",
            "studentID": self.student.ID,
            "studentName": f"{self.student.firstname} {self.student.lastname}",
            "created": self.date_created.strftime("%d-%m-%Y %H:%M"),
            "points": self.points,
            "details": self.details,
            "rating": self.rating,
        }
