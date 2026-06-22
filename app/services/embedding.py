from app.embeddings.base import EmbeddingProvider


class EmbeddingService:


    def __init__(
        self,
        provider: EmbeddingProvider
    ):

        self.provider = provider



    def encode_text(
        self,
        text: str
    ):

        return (
            self.provider
            .encode_text(text)
        )