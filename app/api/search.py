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



@router.get(
    "/search",
    response_model=SearchResponse
)
def search_images(
    query: str,
    page: int = 1,
    limit: int = 12,
    db: Session = Depends(get_db),
    embedding_provider: EmbeddingProvider = Depends(get_embedding_provider),
    vector_store: VectorStore = Depends(get_vector_store)
):

    search_service = SearchService(
        db,
        embedding_provider,
        vector_store
    )

    results = search_service.search(
        query,
        page,
        limit
    )

    return {
        "query": query,
        "results": results
    }



@router.get(
    "/search-preview",
    response_class=HTMLResponse
)
def search_preview(
    query: str = "",
    page: int = 1,
    limit: int = 12,
    db: Session = Depends(get_db),
    embedding_provider: EmbeddingProvider = Depends(get_embedding_provider),
    vector_store: VectorStore = Depends(get_vector_store)
):

    results = []

    if query:

        search_service = SearchService(
            db,
            embedding_provider,
            vector_store
        )

        results = search_service.search(
            query,
            page,
            limit
        )


    html = f"""
    <html>

        <head>

            <style>

                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                }}


                .logo {{
                    position: fixed;
                    top: 20px;
                    right: 30px;
                    width: 90px;
                }}


                .search-box {{
                    text-align: center;
                    margin-bottom: 40px;
                }}


                input {{
                    width: 400px;
                    padding: 12px;
                    font-size: 16px;
                    border-radius: 8px;
                }}


                button {{
                    padding: 12px 20px;
                    font-size: 16px;
                    border-radius: 8px;
                    cursor: pointer;
                }}


                .grid {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 25px;
                }}


                .card {{
                    width: 260px;
                }}


                img.result-image {{
                    width: 260px;
                    height: 260px;
                    object-fit: cover;
                    border-radius: 12px;
                }}


                h4 {{
                    font-size: 14px;
                    word-break: break-word;
                }}


                .pagination {{
                    margin-top: 40px;
                    display: flex;
                    justify-content: center;
                    gap: 15px;
                }}


                .pagination a {{
                    font-size: 18px;
                    text-decoration: none;
                }}

            </style>

        </head>

        <body>

            <img class="logo" src="/static/sire-logo.png">

            <div class="search-box">

                <h2>
                    Semantic Image Retrieval Engine
                </h2>

                <form action="/api/search-preview" method="get">

                    <input
                        type="text"
                        name="query"
                        value="{query}"
                        placeholder="Search images..."
                    >

                    <button type="submit">Search</button>

                </form>

            </div>

            <h3>Results for: {query}</h3>

            <div class="grid">

    """



    for image in results:

        html += f"""

            <div class="card">

                <img class="result-image" src="{image["image_url"]}">

                <h4>{image["file_name"]}</h4>

            </div>

        """



    html += """

            </div>

            <div class="pagination">

    """


    if query:

        for page_number in range(1, 8):

            html += f"""

                <a href="/api/search-preview?query={query}&page={page_number}&limit={limit}">
                {page_number}
                </a>

            """



    html += """

            </div>

        </body>


    </html>

    """

    return html