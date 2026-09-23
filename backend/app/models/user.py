from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    age = Column(Integer, nullable=False)

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False
    )

    organization = relationship("Organization", back_populates="users")
