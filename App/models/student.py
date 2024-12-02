from App.database import db
from .user import User


class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    UniId = db.Column(db.String(10), nullable=False)
    degree = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(255), nullable=True)
    karma = db.Column(db.Integer, nullable=True, default=0)  # Default to 0

    __mapper_args__ = {"polymorphic_identity": "student"}

    def __init__(self, username, UniId, first_name, last_name, email, password, faculty, degree, karma=0):
        super().__init__(username=username,
                         firstname=first_name,
                         lastname=last_name,
                         email=email,
                         password=password,
                         faculty=faculty)
        self.UniId = UniId
        self.degree = degree
        self.full_name = f"{first_name} {last_name}"
        self.karma = karma

    def get_id(self):
        return self.id  # Use lowercase 'id'

    def to_json(self):
        return {
            "studentID": self.id,  # Use lowercase 'id'
            "username": self.username,
            "fullName": self.full_name,
            "degree": self.degree,
            "uniId": self.UniId,  # Use correct attribute name
            "karma": self.karma,
        }
