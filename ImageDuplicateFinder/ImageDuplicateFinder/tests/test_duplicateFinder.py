import pytest
from unittest.mock import MagicMock
from ImageDuplicateFinder.model.duplicateFinder import DuplicateFinder
from ImageDuplicateFinder.model.imageFolder import ImageFolder
from ImageDuplicateFinder.model.image import Image

@pytest.fixture
def mock_image_folder():
    mock_folder = MagicMock(spec=ImageFolder)
    mock_folder.images = [MagicMock(spec=Image) for _ in range(5)]
    for i, img in enumerate(mock_folder.images):
        img.compute_hash.return_value = f'hash_{i}'
        img.hash = f'hash_{i}'
    return mock_folder

def test_find_duplicates(mock_image_folder):
    duplicates = DuplicateFinder.find_duplicates(mock_image_folder)
    assert len(duplicates) == 0

def test_compare_folders(mock_image_folder):
    folder1 = mock_image_folder
    folder2 = mock_image_folder
    duplicates = DuplicateFinder.compare_folders(folder1, folder2)
    assert len(duplicates) == 5
