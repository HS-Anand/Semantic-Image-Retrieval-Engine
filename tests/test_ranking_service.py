from app.services.ranking import RankingService
from types import SimpleNamespace


def test_empty_candidates_returns_empty_list():

    print("\n===== TEST: EMPTY CANDIDATE HANDLING =====")

    service = RankingService()

    result = service.rank([], [])

    assert result == []


def test_low_similarity_returns_empty_list():

    print("\n===== TEST: LOW SIMILARITY QUERY REJECTION =====")

    service = RankingService()

    candidates = [(1, 0.24), (2, 0.23)]

    features = [
        SimpleNamespace(faiss_id=1, quality_score=0.8),
        SimpleNamespace(faiss_id=2, quality_score=0.5)
    ]

    result = service.rank(candidates, features)

    assert result == []


def test_quality_score_does_not_override_similarity():

    print("\n===== TEST: QUALITY DOES NOT OVERRIDE SIMILARITY =====")

    service = RankingService()

    candidates = [(1, 0.90), (2, 0.89)]

    features = [
        SimpleNamespace(
            faiss_id=1,
            quality_score=0.1
        ),
        SimpleNamespace(
            faiss_id=2,
            quality_score=0.9
        )
    ]

    result = service.rank(candidates, features)

    assert result == [1, 2]


def test_missing_quality_defaults_to_zero():

    print("\n===== TEST: DEFAULT QUALITY SCORE FALLBACK =====")

    service = RankingService()

    candidates = [(1, 0.90), (2, 0.88)]

    features = [
        SimpleNamespace(
            faiss_id=1,
            quality_score=0.6
        )
    ]

    result = service.rank(candidates, features)

    assert result == [1, 2]