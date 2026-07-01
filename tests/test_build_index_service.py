import tempfile
from pathlib import Path
from unittest.mock import Mock

from app.services.index_builder import BuildIndexService


def create_service():

    repository = Mock()
    repository.get_next_faiss_id.return_value = 0
    repository.exists_by_file_name.return_value = False

    return BuildIndexService(
        storage=Mock(),
        embedding_provider=Mock(),
        index_builder=Mock(),
        repository=repository,
        quality_scorer=Mock()
    )


def test_invalid_dataset_path_exits_gracefully():

    print("\n===== TEST: INVALID DATASET PATH =====")

    service = create_service()

    service.index_folder(
        "invalid/path",
        "test.index"
    )


def test_empty_dataset_exits_gracefully():

    print("\n===== TEST: EMPTY DATASET HANDLING =====")

    service = create_service()

    with tempfile.TemporaryDirectory() as folder:

        service.index_folder(
            folder,
            "test.index"
        )


def test_corrupted_images_are_skipped():

    print("\n===== TEST: CORRUPTED IMAGE SKIPPING =====")

    service = create_service()

    with tempfile.TemporaryDirectory() as folder:

        image = Path(folder) / "test.jpg"

        image.touch()

        service._is_valid_image = Mock(return_value=False)

        service.index_folder(
            folder,
            "test.index"
        )

        service.embedding_provider.encode_images.assert_not_called()

        service.storage.upload_many.assert_not_called()

        service.index_builder.add_many.assert_not_called()

        service.repository.create_many.assert_not_called()