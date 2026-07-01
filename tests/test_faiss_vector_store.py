import tempfile

import pytest
import numpy as np

from app.indexing.faiss_builder import FAISSIndexBuilder
from app.vector_store.faiss_store import FAISSVectorStore


def test_missing_faiss_index_raises_error():

    print("\n===== TEST: MISSING FAISS INDEX =====")

    with pytest.raises(RuntimeError):

        FAISSVectorStore(
            "missing.index"
        )


def test_returns_stored_faiss_ids():

    print("\n===== TEST: FAISS ID RETRIEVAL =====")

    with tempfile.TemporaryDirectory() as folder:

        index_path = f"{folder}/test.index"

        builder = FAISSIndexBuilder(index_path)

        vectors = [
            np.random.rand(512).astype("float32"),
            np.random.rand(512).astype("float32")
        ]

        builder.add_many(
            vectors,
            [101, 202]
        )

        builder.save(index_path)

        store = FAISSVectorStore(index_path)

        results = store.search(
            vectors[0],
            k=2
        )

        returned_ids = [
            image_id
            for image_id, score in results
        ]

        assert 101 in returned_ids
        assert 202 in returned_ids