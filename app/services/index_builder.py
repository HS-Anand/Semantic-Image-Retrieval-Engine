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
        self,
        folder_path: str,
        output_index_path: str,
        batch_size: int = 64
    ):


        print("START INDEX")


        next_faiss_id = (
            self.repository.get_next_faiss_id()
        )


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


            if self.repository.exists_by_file_name(
                file_name
            ):
                print(
                    "SKIPPING",
                    file_name
                )

                continue


            all_files.append(
                file_name
            )


        print(
            "FILES TO INDEX:",
            len(all_files)
        )



        for start in range(
            0,
            len(all_files),
            batch_size
        ):


            batch_files = all_files[
                start:start + batch_size
            ]


            print(
                "PROCESSING BATCH",
                start,
                "-",
                start + len(batch_files)
            )



            image_paths = [
                os.path.join(
                    folder_path,
                    file_name
                )

                for file_name in batch_files
            ]



            print("QUALITY START")


            quality_scores = [

                self.quality_scorer.score(
                    path
                )

                for path in image_paths
            ]


            print("QUALITY DONE")



            print("CLIP START")


            vectors = (
                self.embedding_provider
                .encode_images(
                    image_paths
                )
            )


            print("CLIP DONE")



            print("CLOUDINARY START")


            urls = (
                self.storage.upload_many(
                    image_paths
                )
            )


            print("CLOUDINARY DONE")



            faiss_ids = list(
                range(
                    next_faiss_id,
                    next_faiss_id + len(batch_files)
                )
            )



            print("FAISS START")


            self.index_builder.add_many(
                vectors,
                faiss_ids
            )


            print("FAISS DONE")



            db_rows = []


            for i in range(
                len(batch_files)
            ):


                db_rows.append(
                    {
                        "faiss_id": faiss_ids[i],

                        "file_name": batch_files[i],

                        "image_url": urls[i],

                        "quality_score": quality_scores[i]
                    }
                )



            print("POSTGRES START")


            self.repository.create_many(
                db_rows
            )


            print("POSTGRES DONE")



            next_faiss_id += len(
                batch_files
            )



            print("SAVE CHECKPOINT\n")


            self.index_builder.save(
                output_index_path
            )



        print("FINAL SAVE")


        self.index_builder.save(
            output_index_path
        )