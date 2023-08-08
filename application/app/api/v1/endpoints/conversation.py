from fastapi import APIRouter, Depends, status, HTTPException

from app.crud.conversation import ConversationCrud
from app.schemas.conversation_schema import ConversationCreate, ConversationBase
from app.api.dependencies import get_current_user, get_conversation_crud

router = APIRouter()


@router.post("/conversations", response_model=ConversationBase)
def create_conversation(
    conversation: ConversationCreate,
    user=Depends(get_current_user),
    conversation_crud: ConversationCrud = Depends(get_conversation_crud),
):
    conversation_model = conversation_crud.create_conversation(user.id, conversation)
    return ConversationBase(
        slug=conversation_model.slug,
        title=conversation_model.title,
        tags=conversation_model.tags,
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationBase)
def get_conversation(
    conversation_id: str,
    user=Depends(get_current_user),
    conversation_crud: ConversationCrud = Depends(get_conversation_crud),
):
    conversation_model = conversation_crud.get_conversation_by_id(conversation_id)
    return conversation_model


@router.get("/conversations/me/", response_model=ConversationBase)
def get_my_conversation(
    user=Depends(get_current_user),
    conversation_crud: ConversationCrud = Depends(get_conversation_crud),
):
    breakpoint()
    conversations = conversation_crud.get_conversations_of_user(user.id)
    return conversations
