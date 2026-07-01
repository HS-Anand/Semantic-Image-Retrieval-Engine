from unittest.mock import Mock, patch

from app.services.search import SearchService


def test_empty_query_returns_empty_list():

    print("\n===== TEST: EMPTY QUERY HANDLING =====")

    service = SearchService(
        db=Mock(),
        embedding_provider=Mock(),
        vector_store=Mock()
    )

    result = service.search("   ")

    assert result == []


@patch("app.services.search.ImageRepository")
@patch("app.services.search.RankingService")
def test_successful_search_pipeline(
    mock_ranking_service,
    mock_image_repository
):

    print("\n===== TEST: SUCCESSFUL SEARCH PIPELINE =====")

    embedding_provider = Mock()
    vector_store = Mock()

    embedding_provider.encode_text.return_value = [0.1, 0.2]

    vector_store.search.return_value = [(1, 0.91), (2, 0.88)]

    repository = mock_image_repository.return_value

    repository.get_ranking_features.return_value = [
        Mock(faiss_id=1, quality_score=0.8),
        Mock(faiss_id=2, quality_score=0.5)
    ]

    mock_ranking_service.return_value.rank.return_value = [1, 2]

    repository.hydrate_results.return_value = [
        {
            "id": "1",
            "faiss_id": 1
        }
    ]

    service = SearchService(
        db=Mock(),
        embedding_provider=embedding_provider,
        vector_store=vector_store
    )

    result = service.search("blue shirt")

    assert result == [
        {
            "id": "1",
            "faiss_id": 1
        }
    ]

    embedding_provider.encode_text.assert_called_once()

    vector_store.search.assert_called_once()

    repository.get_ranking_features.assert_called_once()

    repository.hydrate_results.assert_called_once()


@patch("app.services.search.ImageRepository")
def test_search_failure_raises_runtime_error(
    mock_image_repository
):

    print("\n===== TEST: SEARCH FAILURE HANDLING =====")

    embedding_provider = Mock()

    vector_store = Mock()

    embedding_provider.encode_text.side_effect = Exception(
        "CLIP failed"
    )

    service = SearchService(
        db=Mock(),
        embedding_provider=embedding_provider,
        vector_store=vector_store
    )

    try:

        service.search("blue shirt")

        assert False

    except RuntimeError as e:

        assert str(e) == "Search failed."