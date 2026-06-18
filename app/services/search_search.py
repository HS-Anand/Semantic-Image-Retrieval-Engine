from app.embeddings.base import EmbeddingProvider
from app.vector_store.base import VectorStore

from app.services.ranking import RankingService
from app.repositories.image_repository import ImageRepository


class SearchService:

    def __init__(
        self,
        db,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore
    ):

        self.embedding_provider = embedding_provider

        self.vector_store = vector_store

        self.ranking_service = RankingService()

        self.image_repository = ImageRepository(db)


    def search(self, query: str):

        query_vector = (
            self.embedding_provider
            .encode_text(query)
        )


        candidates = (
            self.vector_store.search(
                query_vector,
                k=5
            )
        )


        candidate_ids = [
            image_id
            for image_id, similarity in candidates
        ]


        features = (
            self.image_repository
            .get_ranking_features(
                candidate_ids
            )
        )


        ranked_ids = (
            self.ranking_service.rank(
                candidates,
                features
            )
        )


        results = (
            self.image_repository
            .hydrate_results(
                ranked_ids
            )
        )


        return results