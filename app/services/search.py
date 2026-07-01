from app.embeddings.base import EmbeddingProvider
from app.vector_store.base import VectorStore

from app.services.ranking import RankingService
from app.repositories.image_repository import ImageRepository

from app.utils.timer import Timer
from app.utils.logger import query_logger, error_logger


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


    def search(
        self,
        query: str,
        page: int = 1,
        limit: int = 12
    ):

        if not query.strip():
            query_logger.info(f'Query completed. Results=0')
            error_logger.info(f'Empty query in search')
            return []

        page = max(page, 1)
        limit = max(limit, 1)

        query_logger.info(f'Query="{query}" Page={page} Limit={limit}')

        try:

            with Timer("TOTAL SEARCH"):

                with Timer("TEXT EMBEDDING"):

                    query_vector = (
                        self.embedding_provider
                        .encode_text(query)
                    )


                with Timer("FAISS SEARCH"):

                    candidates = (
                        self.vector_store.search(query_vector,k=200)
                    )

                candidate_ids = [
                    image_id
                    for image_id, similarity in candidates
                ]


                with Timer("FETCH RANKING FEATURES"):

                    features = (
                        self.image_repository
                        .get_ranking_features(candidate_ids)
                    )


                with Timer("RANKING"):

                    ranked_ids = (
                        self.ranking_service.rank(candidates, features)
                    )


                with Timer("PAGINATION"):

                    start = (page - 1) * limit
                    end = start + limit

                    ranked_ids = ranked_ids[start:end]


                with Timer("POSTGRES HYDRATION"):

                    results = (
                        self.image_repository
                        .hydrate_results(ranked_ids)
                    )

                query_logger.info(f'Query completed. Results={len(results)}')
                return results

        except Exception:
            error_logger.info('Search failed')
            raise RuntimeError("Search failed.")