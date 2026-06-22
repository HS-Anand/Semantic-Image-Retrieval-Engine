from app.vector_store.base import VectorStore


class VectorService:


    def __init__(
        self,
        vector_store: VectorStore
    ):

        self.vector_store = vector_store



    def search(
        self,
        vector,
        k
    ):

        return (
            self.vector_store
            .search(
                vector,
                k
            )
        )