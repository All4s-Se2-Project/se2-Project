from App.database import Base
from .user import User
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey


class Student(User):
  __tablename__ = 'student'
  ID = Column(Integer, ForeignKey("user.ID"), primary_key=True)
  UniId = Column(String(10), nullable=False)
  degree = Column(String(120), nullable=False)
  fullname = Column(String(255), nullable=True)
  admittedTerm = Column(String(120), nullable=False)
  gpa = Column(String(120), nullable=True)

  reviews = relationship("Review", backref="studentReviews", lazy="joined")
  accomplishments = relationship("Accomplishment", backref="studentAccomplishments", lazy="joined")
  incidents = relationship("IncidentReport", backref="studentIncidents", lazy="joined")
  grades = relationship("Grades", backref="studentGrades", lazy="joined")
  transcripts = relationship("Transcript", backref="student", lazy="joined")
  badges = relationship("Badges", backref="studentBadge", lazy="joined")
  karmaID = Column(Integer, ForeignKey("karma.karmaID"))

  __mapper_args__ = {"polymorphic_identity": "student"}

  def __init__(
        self,
        username: str,
        UniId: str,
        firstname: str,
        lastname: str,
        email: str,
        password: str,
        faculty: str,
        admittedTerm: str,
        degree: str,
        gpa: str = None,
    ):
        super().__init__(
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,
            faculty=faculty,
        )
        self.UniId = UniId
        self.degree = degree
        self.admittedTerm = admittedTerm
        self.gpa = gpa
        self.fullname = f"{firstname} {lastname}"

  def get_id(self):
    return self.ID

  # Gets the student details and returns in JSON format
  def to_json(self, karma=None) -> dict:
        return {
            "studentID": self.ID,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "fullname": self.fullname,
            "gpa": self.gpa,
            "email": self.email,
            "faculty": self.faculty,
            "degree": self.degree,
            "admittedTerm": self.admittedTerm,
            "UniId": self.UniId,
            "accomplishments": [
                accomplishment.to_json() for accomplishment in self.accomplishments
            ],
            "incidents": [incident.to_json() for incident in self.incidents],
            "grades": [grade.to_json() for grade in self.grades],
            "transcripts": [transcript.to_json() for transcript in self.transcripts],
            "karmaScore": karma.points if karma else None,
            "karmaRank": karma.rank if karma else None,
        }
