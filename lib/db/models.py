#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')

Base = declarative_base()

class Info(Base):
    __tablename__ = 'information'



    id = Column(Integer(), primary_key = True)
    name = Column(String())

    def __repr__(self):
        return f'Info {self.id}: ' \
        + f"{self.name}"
        


