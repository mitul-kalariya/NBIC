from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, String, Text, DateTime

from app.models.base_model import TimeStampModel
from app.db.base_class import Base


class Conference(Base):
    __tablename__ = "conference"

    title = Column(String, nullable=False)
    objectID = Column(String(10), primary_key=True, index=True)
    summary = Column(Text, nullable=False)
    conference_info = Column(Text, nullable=False)
    location = Column(String(300), nullable=True)
    primary_product = Column(Text, nullable=True)
    secondary_product = Column(Text, nullable=True)
    conference_source = Column(String(10))
    conference_full_details = Column(Text)
    conference_url = Column(String(length=500))
    date = Column(DateTime, nullable=True)
    primary_author = Column(Text, nullable=True)
