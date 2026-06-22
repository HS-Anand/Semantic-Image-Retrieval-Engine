from app.indexing.faiss_builder import FAISSIndexBuilder


builder = FAISSIndexBuilder()


vector = [0.5] * 512


builder.add(
    vector,
    100
)


builder.save(
    "storage/test_new.index"
)


print("done")