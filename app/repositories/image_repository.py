
from app.database.models import ImageAsset
from sqlalchemy import func

class ImageRepository:

    def __init__(self, db):

        self.db = db

    def get_next_faiss_id(self):

        max_id = (
            self.db.query(
                func.max(ImageAsset.faiss_id)
            ).scalar()
        )

        if max_id is None:
            return 0

        return max_id + 1

    def get_ranking_features(self, faiss_ids):

        return (
            self.db
            .query(
                ImageAsset.faiss_id,
                ImageAsset.quality_score
            )
            .filter(
                ImageAsset.faiss_id.in_(faiss_ids)
            )
            .all()
        )


    def hydrate_results(self, faiss_ids):

        results = (
            self.db
            .query(
                ImageAsset.id,
                ImageAsset.faiss_id,
                ImageAsset.file_name,
                ImageAsset.image_url
            )
            .filter(
                ImageAsset.faiss_id.in_(faiss_ids)
            )
            .all()
        )


        return [
            {
                "id": str(result.id),
                "faiss_id": result.faiss_id,
                "file_name": result.file_name,
                "image_url": result.image_url
            }

            for result in results
        ]

    def create(
        self,
        faiss_id: int,
        file_name: str,
        image_url: str,
        quality_score: float,
        category: str = None
    ):

        image = ImageAsset(
            faiss_id=faiss_id,
            file_name=file_name,
            image_url=image_url,
            quality_score=quality_score,
            category=category,
            index_status="INDEXED"
        )


        self.db.add(image)

        self.db.commit()

        self.db.refresh(image)


        return image 