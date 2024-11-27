from App.database import Base
from .user import User
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey


class Staff(User):
    __tablename__ = 'staff'
    ID = Column(Integer, ForeignKey('user.ID'), primary_key=True)
    reviews = relationship('Review', backref='staffReviews', lazy='joined')
    reports = relationship('IncidentReport', backref='staffReports', lazy='joined')
    pendingAccomplishments = relationship(
        'Accomplishment',
        backref='studentAccomplishments',
        lazy='joined'
    )

    __mapper_args__ = {"polymorphic_identity": "staff"}

    def __init__(self, username, firstname, lastname, email, password, faculty):
        super().__init__(
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,
            faculty=faculty
        )

    def to_json(self) -> dict:
        return {
            "staffID": self.ID,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "faculty": self.faculty,
            "reviews": [review.to_json() for review in self.reviews],
            "reports": [report.to_json() for report in self.reports],
            "pendingAccomplishments": [
                pendingAccomplishment.to_json()
                for pendingAccomplishment in self.pendingAccomplishments
            ]
        }

    def __repr__(self):
        return f'<Staff {self.ID}: {self.email}>'
