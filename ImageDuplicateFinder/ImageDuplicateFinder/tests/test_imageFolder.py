import pytest
from PIL import Image as PILImage
from ImageDuplicateFinder.model.imageFolder import ImageFolder


@pytest.fixture
def mock_image_folder(tmp_path):
    folder = tmp_path / "images"
    folder.mkdir()

    for ext in ['.jpg', '.png', '.bmp', '.gif', '.jpeg']:
        img = PILImage.new('RGB', (10, 10), color='red')
        img.save(folder / f"test{ext}")

    return folder


def test_load_images(mock_image_folder):
    folder = ImageFolder(str(mock_image_folder))
    assert len(folder.images) == 5
