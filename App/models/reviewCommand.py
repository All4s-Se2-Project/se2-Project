from App.database import db
from abc import ABCMeta, abstractmethod

class reviewCommand(db.Model, metaclass=ABCMeta):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.ID'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('staff.ID'), nullable=False)

    staff = db.relationship('Staff', backref="reviews")
    student = db.relationship("Student", backref="reviews")
    
    @abstractmethod
    def execute(self):
        pass
    
    def logChange(self):
        pass
