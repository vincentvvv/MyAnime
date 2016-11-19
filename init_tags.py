from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Anime, Tag, tags

engine = create_engine('sqlite:///listofanime.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Initialize Tags
tag = Tag(name="Comedy")
session.add(tag)
session.commit()
tag = Tag(name="Shoen")
session.add(tag)
session.commit()
tag = Tag(name="Action")
session.add(tag)
session.commit()
tag = Tag(name="Gore")
session.add(tag)
session.commit()
tag = Tag(name="Horror")
session.add(tag)
session.commit()
tag = Tag(name="Romance")
session.add(tag)
session.commit()

print("Initialized tags in DB!")