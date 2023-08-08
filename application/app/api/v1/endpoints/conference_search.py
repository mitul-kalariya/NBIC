from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from langchain.vectorstores import VectorStore

from app.db.session import engine
from app.db.base_class import Base
from app.api.dependencies import get_db, get_vector_db

from app.schemas.langchain_schemas.conference_schema import (
    ConferenceResponseSchema,
    ConferenceSchema,
    ConferenceDataSchema,
)

from app.schemas.langchain_schemas.user_query_schema import UserQuerySchema
from app.models.conference_models import Conference
from app.utils.qna_utils import (
    get_answer,
    get_sources,
)

from app.utils.constants import (
    VectorDatabaseConstants,
)


Base.metadata.create_all(bind=engine)

router = APIRouter()


# TODO: have a uniform processing of conference data and generic document search
@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=ConferenceResponseSchema,
)
def larvol_search(
    user_query: UserQuerySchema,
    db: Session = Depends(get_db),
    vector_db: VectorStore = Depends(get_vector_db),
):
    user_query = user_query.user_query

    relevant_documents = vector_db.search_documents(
        user_query,
        VectorDatabaseConstants.TOP_K_DOCUMENTS.value,
        query_preprocessing=True,
    )

    answer = get_answer(relevant_documents, user_query)
    sources = get_sources(answer)

    # Fetch the conferences from the database using the object IDs
    conferences = db.query(Conference).filter(Conference.objectID.in_(sources)).all()

    # Serialize the conferences using the Pydantic model
    serialized_conferences = [
        ConferenceSchema(**conference.__dict__, source=conference.conference_url)
        for conference in conferences
    ]

    return ConferenceResponseSchema(
        success=True,
        message="Response",
        data=ConferenceDataSchema(
            chat_gpt_answer=answer["output_text"].split("SOURCES:")[0],
            answer=serialized_conferences,
        ),
    )
