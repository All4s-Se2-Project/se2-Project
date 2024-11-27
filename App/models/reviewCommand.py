from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase
from sqlalchemy import Column, Integer, ForeignKey
from abc import ABC, abstractmethod
from App.database import db

Base = declarative_base()

class AbstractBase(AbstractConcreteBase, Base):
    __abstract__ = True

class reviewCommand(AbstractBase, ABC):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    staff_id = Column(Integer, ForeignKey('staff.ID'), nullable=False)
    student_id = Column(Integer, ForeignKey('staff.ID'), nullable=False)

    @abstractmethod
    def execute(self):
        pass

    def logChange(self):
        pass
