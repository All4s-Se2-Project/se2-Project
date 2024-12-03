from App.database import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, DateTime
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    created_by_staff_id = Column(Integer, ForeignKey('staff.id'), nullable=False)
    is_positive = Column(Boolean, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    points = Column(Integer, nullable=False)
    details = Column(String(400), nullable=False)
    rating = Column(Integer, nullable=False)

    student = relationship('Student', backref='reviews', lazy=True)
    staff = db.relationship('Staff', backref='reviews_handled', overlaps="reviewing_staff,reviews") 
    rating_commands = relationship("RatingCommand", back_populates="review")
    commands = relationship("ReviewCommand", back_populates="review", overlaps='rating_commands')

    def __init__(self, staff, student, is_positive, rating, points, details):
        self.created_by_staff_id = staff.id
        self.student_id = student.id
        self.is_positive = is_positive
        self.points = points
        self.details = details
        self.date_created = datetime.utcnow()
        self.rating = rating

    def to_json(self):
        return {
            "reviewID": self.id,
            "reviewer": f"{self.staff.first_name} {self.staff.last_name}",
            "studentID": self.student.id,
            "studentName": f"{self.student.first_name} {self.student.last_name}",
            "created": self.date_created.strftime("%d-%m-%Y %H:%M"),
            "points": self.points,
            "details": self.details,
            "rating": self.rating,
        }
