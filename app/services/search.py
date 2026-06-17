from app.services.embedding import EmbeddingService
from app.services.vector import VectorService
from app.services.ranking import RankingService

from app.repositories.image_repository import ImageRepository


class SearchService:

    def __init__(self, db):

        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()
        self.ranking_service = RankingService()

        self.image_repository = ImageRepository(db)


    def search(self, query: str):

        query_vector = self.embedding_service.encode_text(query)

        candidates = self.vector_service.search(query_vector)


        candidate_ids = [
            item["id"] for item in candidates
        ]


        features = (
            self.image_repository.get_ranking_features(candidate_ids)
        )


        ranked_ids = (
            self.ranking_service.rank(candidates, features)
        )


        results = (
            self.image_repository.hydrate_results(ranked_ids)
        )


        return results