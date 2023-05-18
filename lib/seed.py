# !/usr/bin/env python3

from sqlalchemy.orm import sessionmaker
from faker import Faker
from sqlalchemy import create_engine
from db.models import Info, Base
from db.bikes import Bike
from db.locations import Locker

fake = Faker()
database_path = "db/bikedatabase.db"


if __name__ == "__main__":
    engine = create_engine(f"sqlite:///{database_path}")
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
        id=fake.random_int(min=10000, max=99999), name=fake.color_name(), available=True
    )
    for n in range(12)
]

locker = [Locker(locker_location=fake.address()) for i in range(5)]

session.add_all(bike + locker)
session.commit()
