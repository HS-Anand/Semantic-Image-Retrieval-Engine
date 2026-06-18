import faiss
import numpy as np


# CLIP embedding size
dimension = 512


# create FAISS index
index = faiss.IndexFlatIP(
    dimension
)


# allow custom IDs
index = faiss.IndexIDMap(
    index
)


vectors = np.random.random(
    (5, dimension)
).astype("float32")


faiss.normalize_L2(
    vectors
)


ids = np.array(
    [101, 102, 103, 104, 105]
)


index.add_with_ids(
    vectors,
    ids
)


faiss.write_index(
    index,
    "storage/test.index"
)


print("created FAISS index")