from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from project.setup.db import models


class Favorite(models.Base):
    __tablename__ = 'favorites'

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    movie = relationship("Movie")
