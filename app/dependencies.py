from app.vector_store.faiss_store import FAISSVectorStore
from app.embeddings.clip_provider import CLIPProvider


vector_store = FAISSVectorStore("storage/image.index")

embedding_provider = CLIPProvider()


def get_embedding_provider():
    return embedding_provider


def get_vector_store():
    return vector_store