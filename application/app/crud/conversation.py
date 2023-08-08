from typing import Optional, List
from sqlalchemy.orm import Session, joinedload

from app.models import Conversation
from app.schemas.conversation_schema import ConversationCreate, ConversationUpdate


class ConversationCrud:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_conversation_by_id(
        self, conversation_id: str, with_messages: bool = False
    ) -> Optional[Conversation]:
        query = self.db.query(Conversation).filter(Conversation.id == conversation_id)

        if with_messages:
            query = query.options(joinedload(Conversation.messages))

        return query.first()

    def get_conversations_of_user(self, user_id: str) -> List[Conversation]:
        return self.db.query(Conversation).filter(Conversation.user_id == user_id).all()

    def create_conversation(
        self, user_id: str, conversation: ConversationCreate
    ) -> Conversation:
        conversation_model = Conversation(user_id=user_id, **conversation.dict())
        self.db.add(conversation_model)
        self.db.commit()
        return conversation_model

    def update_conversation(
        self, conversation_id: str, update_data: ConversationUpdate
    ) -> Conversation:
        conversation = self.get_conversation_by_id(conversation_id)
        if not conversation:
            return None

        update_data_dict = update_data.dict(exclude_unset=True)
        for key, value in update_data_dict.items():
            setattr(conversation, key, value)

        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def delete_conversation(self, conversation_model) -> Conversation:
        self.db.delete(conversation_model)
        self.db.commit()
        return conversation_model
