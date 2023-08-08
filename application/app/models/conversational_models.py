import uuid
from sqlalchemy import Boolean, Column, String, ForeignKey, ARRAY, UUID
from sqlalchemy.orm import relationship

from app.models.base_model import TimeStampModel


class Conversation(TimeStampModel):
    __tablename__ = "conversation"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False)
    tags = Column(ARRAY(String))

    messages = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan"
    )
    user = relationship("User", back_populates="conversations")

    def __repr__(self):
        return f"<Conversation(id={self.id}, title='{self.title}', slug='{self.slug}')>"


class Message(TimeStampModel):
    __tablename__ = "message"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID, ForeignKey("conversation.id"), nullable=False)
    message = Column(String, nullable=False)
    is_agent = Column(Boolean, nullable=False)
    original_prompt = Column(String)

    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return (
            f"<Message(id={self.id}, message='{self.message}', isAgent={self.isAgent})>"
        )
