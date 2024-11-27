from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, Integer, ForeignKey
from abc import ABC, abstractmethod

@as_declarative()
class Base:
    id = Column(Integer, primary_key=True)

class reviewCommand(Base, ABC):
    __tablename__ = 'review_command'
    
    staff_id = Column(Integer, ForeignKey('staff.ID'), nullable=False)
    student_id = Column(Integer, ForeignKey('student.ID'), nullable=False)

    @abstractmethod
    def execute(self):
        pass

    def logChange(self):
        pass
