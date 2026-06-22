import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

from app.database.session import SessionLocal

from app.storage.cloudinary_storage import CloudinaryStorage
from app.embeddings.clip_provider import CLIPProvider
from app.indexing.faiss_builder import FAISSIndexBuilder

from app.quality.scorer import ImageQualityScorer
from app.repositories.image_repository import ImageRepository

from app.services.index_builder import BuildIndexService



db = SessionLocal()


service = BuildIndexService(
    storage=CloudinaryStorage(),

    embedding_provider=CLIPProvider(),

    index_builder=FAISSIndexBuilder(),

    repository=ImageRepository(db),

    quality_scorer=ImageQualityScorer()
)


service.index_folder(
    folder_path="dataset",
    output_index_path="storage/image.index"
)


print("Index build completed")