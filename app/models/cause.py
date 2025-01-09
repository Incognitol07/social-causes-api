# app/models/causes.py

from uuid import uuid4
from sqlalchemy import UUID, String, Column
from sqlalchemy.orm import relationship
from app.database import Base


class Cause(Base):
    __tablename__ = "causes"
    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description =  Column(String, nullable= False)
    image_url = Column(String, nullable=False)

    contributions = relationship("Contribution", back_populates="cause")