import os

from app.storage.base import ImageStorage
from app.embeddings.base import EmbeddingProvider
from app.indexing.base import IndexBuilder

from app.quality.scorer import ImageQualityScorer
from app.repositories.image_repository import ImageRepository

class BuildIndexService:


    def __init__(
        self,
        storage: ImageStorage,
        embedding_provider: EmbeddingProvider,
        index_builder: IndexBuilder,
        repository: ImageRepository,
        quality_scorer: ImageQualityScorer
    ):

        self.storage = storage

        self.embedding_provider = embedding_provider

        self.index_builder = index_builder

        self.repository = repository

        self.quality_scorer = quality_scorer

    def index_folder(
        self, folder_path: str,
        output_index_path: str
        ):

        print("START INDEX")

        faiss_id = (self.repository.get_next_faiss_id())

        print("DB DONE")

        for file_name in os.listdir(folder_path):

            if not file_name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                continue

            print("FILE", file_name)

            image_path = os.path.join(
                folder_path,
                file_name
            )

            print("QUALITY START")

            quality_score = (
                self.quality_scorer.score(image_path)
            )

            print("QUALITY DONE")
            print("CLIP START")

            vector = (
                self.embedding_provider
                .encode_image(image_path)
            )

            print("CLIP DONE")
            print("CLOUDINARY UPLOAD START")


            image_url = (
                self.storage.upload(image_path)
            )
            print("CLOUDINARY DONE")

            print("faiss START")
            self.index_builder.add(
                vector,
                faiss_id
            )
            print("FAISS DONE")

            print("POSTGRE STORE START")
            self.repository.create(
                faiss_id=faiss_id,
                file_name=file_name,
                image_url=image_url,
                quality_score=quality_score
            )
            print("POSTGRE DONE")


            faiss_id += 1


        self.index_builder.save(output_index_path)