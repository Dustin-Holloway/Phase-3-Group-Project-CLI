from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .models import Base


class Bike(Base):
    __tablename__ = "bikes"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    available = Column(Boolean(), default=False)
    user_info = Column(Integer(), ForeignKey("information.id"))
    info = relationship("Info", back_populates="bikes")

    def __repr__(self):
        return f"Bike {self.id}: " + f"{self.name}"
