import os
import pytest
import torch
from torchvision import transforms
from torch.utils.data import DataLoader
from PIL import Image
from unittest.mock import patch
from ImageDuplicateFinder.utils.dataset import CustomImageDataset, create_dataloader, filter_invalid_images


# Fixtures for setting up и tearing down test data
@pytest.fixture
def image_dir(tmp_path):
    # Create a temporary directory with sample images
    for i in range(5):
        img = Image.new('RGB', (60, 30), color=(73, 109, 137))
        img.save(tmp_path / f"image_{i}.jpg")
    return tmp_path


def test_load_image_paths(image_dir):
    dataset = CustomImageDataset(image_dir)
    assert len(dataset) == 5
    for img_path in dataset.image_paths:
        assert os.path.exists(img_path)


def test_getitem(image_dir):
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor()
    ])
    dataset = CustomImageDataset(image_dir, transform=transform)
    img, path = dataset[0]
    assert isinstance(img, torch.Tensor), f"Expected torch.Tensor, got {type(img)}"
    assert img.shape[1] == 256
    assert img.shape[2] == 256
    assert os.path.exists(path)


def test_create_dataloader(image_dir):
    dataloader = create_dataloader(image_dir, batch_size=2)
    batch = next(iter(dataloader))
    images, paths = batch
    assert len(images) == 2
    assert len(paths) == 2
    for img in images:
        assert isinstance(img, torch.Tensor)
    for path in paths:
        assert os.path.exists(path)


def test_filter_invalid_images(image_dir):
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor()
    ])
    dataset = CustomImageDataset(image_dir, transform=transform)
    dataloader = DataLoader(dataset, batch_size=2)
    batch = next(iter(dataloader))

    # Fixing the structure of batch data
    batch = [(img, path) for img, path in zip(*batch)]

    filtered_batch = filter_invalid_images(batch)
    assert len(filtered_batch) == 2
    for img, path in filtered_batch:
        assert isinstance(img, torch.Tensor)
        assert os.path.exists(path)


@patch('ImageDuplicateFinder.utils.dataset.Image.open')
def test_getitem_with_invalid_image(mock_open, image_dir):
    mock_open.side_effect = Exception("Test Exception")
    dataset = CustomImageDataset(image_dir)
    img, path = dataset[0]
    assert img is None
    assert os.path.exists(path)
