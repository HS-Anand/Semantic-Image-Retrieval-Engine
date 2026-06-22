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
from app.schemas.search import SearchResponse

from fastapi.responses import HTMLResponse

router = APIRouter(
    tags=["Search"]
)


@router.get("/health")
def health_check():

    return {
        "status": "running",
        "service": "SIRE"
    }


@router.get("/search", response_model=SearchResponse)
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

@router.get(
    "/search-preview",
    response_class=HTMLResponse
)
def search_preview(
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


    html = f"""
    <html>
        <body>

        <h2>SIRE Results for: {query}</h2>

    """


    for image in results:

        html += f"""

        <div style="margin:20px">

            <h4>{image["file_name"]}</h4>

            <img 
                src="{image["image_url"]}
                "
                width="300"
            >

        </div>

        """


    html += """

        </body>
    </html>

    """


    return html