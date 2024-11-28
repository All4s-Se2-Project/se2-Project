from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from App.models.user import User


class Student(User):
    __tablename__ = 'student'
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    uni_id = Column(String(10), nullable=False)
    degree = Column(String(120), nullable=False)
    full_name = Column(String(255), nullable=True)
    admitted_term = Column(String(120), nullable=False)
    gpa = Column(String(120), nullable=True)

    reviews = relationship("Review", backref="studentReviews", lazy="joined")
    accomplishments = relationship("Accomplishment", backref="studentAccomplishments", lazy="joined")
    incidents = relationship("IncidentReport", backref="studentIncidents", lazy="joined")
    grades = relationship("Grades", backref="studentGrades", lazy="joined")
    transcripts = relationship("Transcript", backref="student", lazy="joined")
    badges = relationship("Badges", backref="studentBadge", lazy="joined")
    karma_id = Column(Integer, ForeignKey("karma.karmaID"))

    __mapper_args__ = {"polymorphic_identity": "student"}

    def __init__(
        self,
        username: str,
        uni_id: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        faculty: str,
        admitted_term: str,
        degree: str,
        gpa: str = None,
    ):
        super().__init__(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            faculty=faculty,
        )
        self.uni_id = uni_id
        self.degree = degree
        self.admitted_term = admitted_term
        self.gpa = gpa
        self.full_name = f"{first_name} {last_name}"

    def get_id(self):
        return self.id

    def to_json(self, karma=None) -> dict:
        return {
            "studentID": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "gpa": self.gpa,
            "email": self.email,
            "faculty": self.faculty,
            "degree": self.degree,
            "admitted_term": self.admitted_term,
            "uni_id": self.uni_id,
            "accomplishments": [
                accomplishment.to_json() for accomplishment in self.accomplishments
            ],
            "incidents": [incident.to_json() for incident in self.incidents],
            "grades": [grade.to_json() for grade in self.grades],
            "transcripts": [transcript.to_json() for transcript in self.transcripts],
            "karma_score": karma.points if karma else None,
            "karma_rank": karma.rank if karma else None,
        }
