import os
import sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

watched = Table('watched', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('anime_id', Integer, ForeignKey('anime.id')),
    Column('finished', Boolean, default=False),
    Column('rate', Integer, default=0))

class User(Base):
    __tablename__ = 'user'
    id       = Column(Integer, primary_key=True)
    name     = Column(String(250), nullable=False)
    watched  = relationship("Anime",
                    secondary=watched,
                    backref="users")

tags = Table('tags', Base.metadata,
    Column('anime_id', Integer, ForeignKey('anime.id')),
    Column('tag_name', String(250), ForeignKey('tag.name'))
)

class Anime(Base):
    __tablename__ = 'anime'
    id          = Column(Integer, primary_key=True)
    name        = Column(String(250), nullable=False)
    episodes    = Column(String(20), nullable =False)
    description = Column(String(20), nullable =False)
    image       = Column(String(250), nullable=False)
    tags        = relationship("Tag",
                    secondary=tags,
                    backref="animes")

    @property
    def serialize(self):
        theTags = []
        for tag in self.tags:
            theTags.append(tag.name)
        print(theTags)
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'tags': theTags,
        }

class Tag(Base):
    __tablename__ = 'tag'
    name          = Column(String(250), primary_key=True)

    @property
    def serialize(self):
        return {
            'name': self.name,
        }

engine = create_engine('sqlite:///listofanime.db')
Base.metadata.create_all(engine)
