from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.models import Base
from db.bikes import bike_locker


class Locker(Base):
    __tablename__ = "lockers"

    id = Column(Integer(), primary_key=True)
    locker_location = Column(String())
    bikes = []
    bikes = relationship("Bike", secondary=bike_locker, back_populates="lockers")

    def __repr__(self):
        return f"Locker {self.id}: " + f"{self.locker_location}"
