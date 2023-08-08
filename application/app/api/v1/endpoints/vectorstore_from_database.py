from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from langchain.vectorstores import VectorStore

from app.api.dependencies import get_db, get_vector_db
from app.crud.base_crud import CRUDBase
from app.models.conference_models import Conference
from app.exception.base_exception import vector_index_not_created

from app.utils.document_utils import dict_to_document
from app.utils.constants import VectorDatabaseConstants


router = APIRouter()


# TODO: take all the pickle and unpickle task in constant file
@router.get("/create-from-database", status_code=status.HTTP_201_CREATED)
def create_embedding_from_database(
    db_session: Session = Depends(get_db),
    vector_db: VectorStore = Depends(get_vector_db),
):
    try:
        crud = CRUDBase(Conference)
        only_included_fields = [
            "title",
            "summary",
            "location",
            "date",
            "primary_author",
            "primary_product",
            "secondary_product",
            "objectID",
        ]
        data_dictionary_list = crud.get_model_data_in_dict(
            db_session=db_session, only_included_fields=only_included_fields
        )
        documents = dict_to_document(data_dictionary_list)
        vector_db.insert_documents(documents)

        return JSONResponse(
            {"message": "index created successfully"}, status_code=status.HTTP_200_OK
        )

    except Exception as e:
        raise vector_index_not_created
