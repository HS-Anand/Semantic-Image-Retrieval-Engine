from app.database.models import ImageAsset


class ImageRepository:

    def __init__(self, db):

        self.db = db


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