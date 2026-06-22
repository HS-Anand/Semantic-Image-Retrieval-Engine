from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.dependencies import (
    get_embedding_provider,
    get_vector_store
)

from app.embeddings.base import EmbeddingProvider
from app.vector_store.base import VectorStore

from app.services.search import SearchService


router = APIRouter(
    tags=["Search"]
)


@router.get("/health")
def health_check():

    return {
        "status": "running",
        "service": "SIRE"
    }


@router.get("/search")
def search_images(
    query: str,

    db: Session = Depends(get_db),

    embedding_provider: EmbeddingProvider = Depends(
        get_embedding_provider
    ),

    vector_store: VectorStore = Depends(
        get_vector_store
    )
):

    search_service = SearchService(
        db,
        embedding_provider,
        vector_store
    )

    results = search_service.search(query)


    return {
        "query": query,
        "results": results
    }