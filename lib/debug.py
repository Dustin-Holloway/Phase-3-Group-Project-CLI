from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Info

if __name__ == '__main__':
    engine = create_engine('sqlite:///one_to_many.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    import ipdb; ipdb.set_trace()
