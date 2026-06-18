from app.vector_store.faiss_store import FAISSVectorStore


store = FAISSVectorStore(
    "storage/test.index"
)


query = [0.5] * 512


print(
    store.search(
        query,
        k=3
    )
)