#!/usr/bin/env python3

from sqlalchemy.orm import sessionmaker
from faker import Faker
from sqlalchemy import create_engine
from models import Info, Base
from bikes import Bike
from locations import Locker


fake = Faker()

if __name__ == '__main__':
    engine = create_engine('sqlite:///bikedatabase.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Bike).delete()
    session.query(Info).delete()
    session.query(Locker).delete()
    session.commit()

print("Seeding bikes...")

bike = [
    Bike(
        name=fake.word()   
    )
for i in range(50)]

stats = [
    Info(
        name=fake.name()
    )
for i in range(50)
]

locker = [
    Locker(
        locker_location=fake.address()
    )
for i in range(25)

]

session.add_all(bike + stats + locker)
session.commit()