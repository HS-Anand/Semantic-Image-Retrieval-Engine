import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from app.api import search


from app.database.session import engine, Base
from app.database import models



Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SIRE API",
    description="Semantic Image Retrieval Engine",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


app.include_router(
    search.router,
    prefix="/api"
)