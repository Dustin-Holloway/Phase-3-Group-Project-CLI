from models import Base
from sqlalchemy import Column, Integer, String



class Bike(Base):
    __tablename__ = 'bikes'


    id = Column(Integer(), primary_key = True)
    name = Column(String())

    def __repr__(self):
        return f'Info {self.id}: ' \
        + f"{self.name}"
        