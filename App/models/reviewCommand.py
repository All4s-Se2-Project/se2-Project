from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from abc import ABC, abstractmethod

Base = declarative_base()

class reviewCommand(Base, ABC):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    staff_id = Column(Integer, ForeignKey('staff.ID'), nullable=False)
    student_id = Column(Integer, ForeignKey('student.ID'), nullable=False)

    staff = relationship('Staff', backref='reviews')
    student = relationship('Student', backref='reviews')

    @abstractmethod
    def execute(self):
        pass

    def logChange(self):
        pass
