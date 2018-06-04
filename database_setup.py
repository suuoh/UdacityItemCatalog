# Configuration
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# User Class
class User(Base):
    # Table
    __tablename__ = "user"

    # Mappings
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    # Serialization
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
        }


# Genre Class
class Genre(Base):
    # Table
    __tablename__ = "genre"

    # Mappings
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    # Serialization
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


# Game Class
class Game(Base):
    # Table
    __tablename__ = "game"

    # Mappings
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    price = Column(String(10))
    developer = Column(String(250))
    release_date = Column(Date)
    platform = Column(String(250))
    genre_id = Column(Integer, ForeignKey("genre.id"))
    genre = relationship(Genre)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)

    # Serialization
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'developer': self.developer,
            'release_date': self.release_date,
            'platform': self.platform,
            'genre_id': self.genre_id,
            'user_id': self.user_id,
        }

# Configuration
engine = create_engine("sqlite:///videogamecatalog.db")

Base.metadata.create_all(engine)
