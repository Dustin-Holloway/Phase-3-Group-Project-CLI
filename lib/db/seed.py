#!/usr/bin/env python3

from sqlalchemy.orm import sessionmaker
from faker import Faker
from sqlalchemy import create_engine
from bikes import Bikes
from models import Info


fake = Faker()

if __name__ == '__main__':

    engine = create_engine('sqlite:///bikedatabase.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Bikes).delete()
    session.query(Info).delete()
    session.commit()

print("Seeding bikes...")

bike = [
    Bikes(
        name=fake.word()   
    )
for i in range(50)]

stats = [
    Info(
        name=fake.name()
    )
for i in range(50)
]

session.add_all(bike + stats)
session.commit()