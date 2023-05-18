from sqlalchemy.orm import sessionmaker
from faker import Faker
from sqlalchemy import create_engine
from db.models import Info, Base
from db.bikes import Bike, bike_locker
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
    session.query(bike_locker).delete()
    session.commit()

    print("Seeding bikes...")

    lockers = []
    for i in range(5):
        locker = Locker(locker_location=fake.address())
        session.add(locker)
        lockers.append(locker)

    session.commit()

    for locker in lockers:
        bikes = [
            Bike(
                name=fake.color_name(),
                available=True,
                id=fake.random_int(min=10000, max=99999),
            )
            for n in range(12)
        ]  # Associate each bike with the current locker
        locker.bikes = bikes
        session.add(locker)

    session.commit()
