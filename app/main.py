from fastapi import FastAPI

from app.api import search


app = FastAPI(
    title="SIRE API",
    description="Semantic Image Retrieval Engine",
    version="1.0.0",
)


app.include_router(
    search.router,
    prefix="/api"
)