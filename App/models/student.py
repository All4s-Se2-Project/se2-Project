from App.database import db
from .user import User


class Student(User):
  __tablename__ = 'student'
  ID = db.Column(db.Integer, db.ForeignKey('user.ID'), primary_key=True)
  uniId = db.Column(db.String(10), nullable=False)
  degree = db.Column(db.String(120), nullable=False)
  full_name = db.Column(db.String(255), nullable=True)
  karma = db.Column(db.Integer, nullable=True)

  __mapper_args__ = {"polymorphic_identity": "student"}

  def __init__(self, username, UniId, first_name, last_name, email, password, faculty, degree, karma=0):
      super().__init__(username=username,
                       firstname=first_name,
                       lastname=last_name,
                       email=email,
                       password=password,
                       faculty=faculty)
      self.uniId = uniId
      self.degree = degree
      self.full_name = f"{first_name} {last_name}"
      self.karma = karma
  
  def get_id(self):
    return self.ID

  # Gets the student details and returns in JSON format
  def to_json(self):
    return{
      "studentID": self.ID,
      "username": self.username,
      "fullName": self.full_name,
      "degree": self.degree,
      "uniId": self.uniId,
      "karma": self.karma,
    }
