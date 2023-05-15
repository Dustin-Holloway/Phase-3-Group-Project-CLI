from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from models import Base



Base = declarative_base()


class Bikes(Base):
    __tablename__ = 'bikes'


    id = Column(Integer(), primary_key=True)
    name = Column(String())

    def __repr__(self):
        return f'Info {self.id}: ' \
        + f"{self.name}"
        

