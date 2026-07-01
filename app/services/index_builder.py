import os

from app.storage.base import ImageStorage
from app.embeddings.base import EmbeddingProvider
from app.indexing.base import IndexBuilder

from app.quality.scorer import ImageQualityScorer
from app.repositories.image_repository import ImageRepository

from app.utils.timer import Timer
from app.utils.logger import index_logger, error_logger

from PIL import Image


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


    def _is_valid_image(self, image_path: str) -> bool:

        try:
            with Image.open(image_path) as image:
                image.verify()
            return True

        except Exception:
            print(f"SKIPPING CORRUPTED IMAGE: {image_path}")
            error_logger.warning(f"Corrupted image skipped: {image_path}")
            return False


    def index_folder(
        self,
        folder_path: str,
        output_index_path: str,
        batch_size: int = 64
    ):
        
        if not os.path.isdir(folder_path):
            print(f"\nDataset folder not found: {folder_path}\n")
            error_logger.warning(f"Dataset folder not found: {folder_path}")
            return


        print("START INDEX")
        index_logger.info("Indexing started")


        next_faiss_id = (self.repository.get_next_faiss_id())

        all_files = []

        for file_name in os.listdir(folder_path):

            if not file_name.lower().endswith(
                (
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".webp"
                )
            ):
                continue


            if self.repository.exists_by_file_name(file_name):
                print("SKIPPING", file_name)
                continue

            all_files.append(file_name)

        if not all_files:
            print("\nNo supported images found.\n")
            error_logger.warning(f"No supported images found in dataset")
            return


        print("FILES TO INDEX:", len(all_files))
        index_logger.info(f"Found {len(all_files)} images to index.")

        for start in range(0, len(all_files), batch_size):

            batch_files = all_files[start:start + batch_size]

            print("PROCESSING BATCH", start, "-", start + len(batch_files))
            index_logger.info(f"Processing batch {start} - {start + len(batch_files)}")

            valid_files = []

            image_paths = []

            for file_name in batch_files:

                image_path = os.path.join(folder_path, file_name)

                if self._is_valid_image(image_path):
                    valid_files.append(file_name)
                    image_paths.append(image_path)

            if not image_paths:
                continue


            print("QUALITY START")

            with Timer("QUALITY"):
                quality_scores = [
                    self.quality_scorer.score(path)
                    for path in image_paths
                ]

            print("QUALITY DONE")


            print("CLIP START")

            with Timer("CLIP BATCH"):
                vectors = (
                    self.embedding_provider
                    .encode_images(image_paths)
                )

            print("CLIP DONE")


            print("CLOUDINARY START")

            with Timer("CLOUDINARY BATCH"):
                urls = (self.storage.upload_many(image_paths))

            print("CLOUDINARY DONE")


            faiss_ids = list(
                range(
                    next_faiss_id,
                    next_faiss_id + len(valid_files)
                )
            )


            print("FAISS START")

            with Timer("FAISS ADD"):
                self.index_builder.add_many(vectors,faiss_ids)

            print("FAISS DONE")


            db_rows = []

            for i in range(len(valid_files)):

                db_rows.append(
                    {
                        "faiss_id": faiss_ids[i],
                        "file_name": valid_files[i],
                        "image_url": urls[i],
                        "quality_score": quality_scores[i]
                    }
                )


            print("POSTGRES START")

            with Timer("POSTGRES BULK INSERT"):
                self.repository.create_many(db_rows)

            print("POSTGRES DONE")


            next_faiss_id += len(valid_files)


            print("SAVE CHECKPOINT\n")

            self.index_builder.save(output_index_path)

            index_logger.info("Checkpoint saved")


        print("FINAL SAVE")

        self.index_builder.save(output_index_path)

        index_logger.info("Indexing completed")