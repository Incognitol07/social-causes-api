# app/models/contribution.py

from uuid import uuid4
from sqlalchemy import UUID, String, Float, Column, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Contribution(Base):
    __tablename__ = "contributions"
    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email =  Column(String, nullable= False)
    amount = Column(Float, nullable=False)
    cause_id = Column(UUID(as_uuid=True), ForeignKey("causes.id"))

    cause = relationship("Cause", back_populates="contributions")