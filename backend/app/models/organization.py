from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    users = relationship("User", back_populates="organization")
