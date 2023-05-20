from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    bike = Column(Integer())
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    def __repr__(self):
        return f"Info {self.id}: " + f"{self.name}"
