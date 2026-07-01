from pydantic import BaseModel, HttpUrl
from typing import List
from uuid import UUID


class ImageResult(BaseModel):

    id: UUID
    faiss_id: int
    file_name: str
    image_url: HttpUrl


class SearchResponse(BaseModel):

    query: str
    results: List[ImageResult]