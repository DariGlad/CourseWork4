from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from project.setup.db import models


class User(models.Base):
    __tablename__ = 'users'

    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    name = Column(String(100))
    surname = Column(String(250))
    favorite_genre = Column(Integer, ForeignKey("genres.id"))
    genre = relationship("Genre")
