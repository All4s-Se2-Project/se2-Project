from App.database import db
from .student import Student
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'review'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.ID'), nullable=False)
    created_by_staff_id = db.Column(db.Integer, db.ForeignKey('staff.ID'), nullable=False)
    is_positive = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    points = db.Column(db.Integer, nullable=False)
    details = db.Column(db.String(400), nullable=False)
    student_seen = db.Column(db.Boolean, default=False, nullable=False)

    student = db.relationship('Student', backref='reviews', lazy=True)
    staff = db.relationship('Staff', backref='reviews_given', lazy=True)

    def __init__(self, staff, student, is_positive, points, details, student_seen=False):
        self.created_by_staff_id = staff.ID
        self.student_id = student.ID
        self.is_positive = is_positive
        self.points = points
        self.details = details
        self.date_created = datetime.utcnow()
        self.student_seen = student_seen

    def get_id(self):
        return self.id

    def mark_as_seen(self):
        """Mark the review as seen by the student."""
        self.student_seen = True
        db.session.commit()

    def to_json(self):
        return {
            "reviewID": self.id,
            "reviewer": f"{self.staff.first_name} {self.staff.last_name}",
            "studentID": self.student.id,
            "studentName": f"{self.student.first_name} {self.student.last_name}",
            "created": self.date_created.strftime("%d-%m-%Y %H:%M"),
            "isPositive": self.is_positive,
            "points": self.points,
            "details": self.details,
            "studentSeen": self.student_seen,
        }
