from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
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
def search_images( query: str, db: Session = Depends(get_db)):

    search_service = SearchService(db)
    results = search_service.search(query)

    return {
        "query": query,
        "results": results
    }