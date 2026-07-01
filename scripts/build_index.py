import os
from app.utils import timer
from app.utils.timer import Timer

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
INDEX_PATH = "storage/image.index"

service = BuildIndexService(
    storage=CloudinaryStorage(),
    embedding_provider=CLIPProvider(),
    index_builder=FAISSIndexBuilder(INDEX_PATH),
    repository=ImageRepository(db),
    quality_scorer=ImageQualityScorer()
)

IMAGE_COUNT = len(
    [
        file for file in os.listdir("dataset")
        if file.lower().endswith(
            (
                ".jpg",
                ".jpeg",
                ".png",
                ".webp"
            )
        )
    ]
)

with Timer("TOTAL INDEXING TIME") as total_timer:

    service.index_folder(
        folder_path="dataset",
        output_index_path=INDEX_PATH
    )


print("Index build completed")


print(
    "Images/sec:",
    round(IMAGE_COUNT / total_timer.duration, 2)
)


print(
    "Images/min:", 
    round((IMAGE_COUNT / total_timer.duration) * 60, 2)
)