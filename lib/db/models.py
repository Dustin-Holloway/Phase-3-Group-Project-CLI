from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# from .bikes import Bike


Base = declarative_base()


class Info(Base):
    __tablename__ = "information"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    bike = Column(Integer())
    bikes = relationship("Bike", back_populates="info")

    def __repr__(self):
        return f"Info {self.id}: " + f"{self.name}"
