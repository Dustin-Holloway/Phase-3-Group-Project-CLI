from sqlalchemy import Column, Integer, String
from models import Base


class Locker(Base):
    __tablename__ = 'lockers'

    id = Column(Integer(), primary_key = True)
    locker_location = Column(String())

    def __repr__(self):
        return f'Locker {self.id}: ' \
        + f"{self.locker_location}"
        

