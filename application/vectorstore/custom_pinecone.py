from typing import List, Optional, Any, Union
import pinecone, os

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.pinecone import Pinecone

from vectorstore.base import CustomBaseVectorStore
from app.utils.constants import VectorDatabaseConstants
from app.utils.document_utils import count_tokens


class CustomPinecone(Pinecone, CustomBaseVectorStore):
    def __init__(
        self,
        embedding_function: Embeddings,
        text_key: str,
        namespace: Optional[str] = None,
    ):
        index = self.connect_to_vectorstore()
        super().__init__(index, embedding_function, text_key, namespace)

    def connect_to_vectorstore(self):
        """code for connecting to pinecone database"""

        pinecone.init(
            api_key=os.environ.get("PINECONE_API_KEY"),
            environment=os.environ.get("PINECONE_ENVIORNMENT"),
        )
        index = pinecone.Index(os.environ.get("PINECONE_INDEX"))
        return index

    def insert_document_with_index(self, id: Any, docs: str, meta: dict = {}):
        """insert single data raw into pinecone database with index"""
        upload_data = []
        meta[self._text_key] = docs
        meta["tokens"] = count_tokens(docs)
        embeddings = self._embedding_function(docs)
        upload_data.append({"id": str(id), "values": embeddings, "metadata": meta})
        return self._index.upsert(vectors=upload_data, namespace=self._namespace)

    def update_document_with_index(self, id: Any, docs: str, meta: dict = {}):
        """update single data raw in pinecone database with given index"""
        meta[self._text_key] = docs
        meta["tokens"] = count_tokens(docs)
        embeddings = self._embedding_function(docs)
        return self._index.update(
            id=str(id), values=embeddings, set_metadata=meta, namespace=self._namespace
        )

    def delete_document_with_index(self, ids: List[Union[str, int]]):
        """delete one or more rows of date in pinecone database with given id(s)"""
        delete_ids = [str(id) for id in ids]
        return self._index.delete(ids=delete_ids, namespace=self._namespace)

    def insert_documents(self, docs: List[Document]):
        """Insert documents into the pinecone database."""

        return self.add_documents(docs)

    def search_documents(
        self, query: str, top_k: int, query_preprocessing: bool = False
    ) -> List[Document]:
        """Search the pinecone database and retrieve relevant documents."""
        if query_preprocessing:
            query = self.preprocess_text(query)

        relevant_documents = self.similarity_search(query, top_k)

        return self._token_safe_documents(
            relevant_documents, query, conversation_history_token=0
        )

    def delete_documents(
        self, ids: Optional[List[str]] = None, namespace: Optional[str] = None
    ):
        """Delete one or more documents from the pinecone database."""
        self._index.delete(ids=ids, namespace=namespace)
        return

    def update_documents(self, docs: List[Document]):
        """Update one or more documents in the pinecone database."""
        raise NotImplementedError("pinecone update method implementation is pending")


custom_pinecone = CustomPinecone(
    embedding_function=VectorDatabaseConstants.VECTOR_EMBEDDING.value.embed_query,
    text_key="langchainn",
    namespace="namespace",
)

nbic_pinecone = CustomPinecone(
    embedding_function=VectorDatabaseConstants.VECTOR_EMBEDDING.value.embed_query,
    text_key="text",
    namespace="nbic",
)
