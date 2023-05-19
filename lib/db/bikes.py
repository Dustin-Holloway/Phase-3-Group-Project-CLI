from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from .users import Base

bike_locker = Table(
    "bike_locker",
    Base.metadata,
    Column("bike_id", ForeignKey("bikes.id"), primary_key=True),
    Column("locker_id", ForeignKey("lockers.id"), primary_key=True),
    extend_existing=True,
)


class Bike(Base):
    __tablename__ = "bikes"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    locker_id = Column(Integer())
    user_id = Column(Integer())

    # adding relationship between bike and locker Id
    # locker = Column(Integer(), ForeignKey("lockers.id"))
    lockers = relationship("Locker", back_populates="bikes")

    lockers = relationship("Locker", secondary=bike_locker, back_populates="bikes")

    def __repr__(self):
        return f"Bike {self.id}: " + f"{self.name}"
