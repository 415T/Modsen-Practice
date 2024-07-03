import pytest
import torch
from torchvision import models
from unittest.mock import patch, MagicMock
from ImageDuplicateFinder.model.duplicateFinderCNN import FeatureExtractor, extract_features, find_duplicates_cnn
import numpy as np
from torchvision.models import ResNet18_Weights


@pytest.fixture
def mock_dataloader():
    images = torch.randn(4, 3, 256, 256)
    paths = [f'image_{i}.jpg' for i in range(4)]
    return [(images, paths)]


def test_feature_extractor():
    weights = ResNet18_Weights.IMAGENET1K_V1
    model = models.resnet18(weights=weights)
    feature_extractor = FeatureExtractor(model)
    x = torch.randn(1, 3, 256, 256)
    features = feature_extractor(x)
    assert features.shape == (1, 512)


# Mocked data for the dataloader and model
@patch('ImageDuplicateFinder.model.duplicateFinderCNN.DataLoader')
@patch('ImageDuplicateFinder.model.duplicateFinderCNN.FeatureExtractor')
def test_extract_features(mock_feature_extractor, mock_dataloader):
    device = torch.device('cpu')

    # Mock the feature extractor model
    mock_model = MagicMock()
    mock_feature_extractor.return_value = mock_model

    # Mock the data returned by the dataloader
    images = torch.randn(4, 3, 256, 256)  # 4 images of 3x256x256
    batch_paths = ['img1', 'img2', 'img3', 'img4']
    mock_dataloader.__iter__.return_value = [(images, batch_paths)]

    # Mock the output of the model
    mock_model.return_value = torch.randn(4, 512)  # Assuming ResNet18-like output

    dataloader = mock_dataloader
    model = mock_feature_extractor()

    features, paths = extract_features(dataloader, model, device)

    assert features.shape == (4, 512)
    assert paths == ['img1', 'img2', 'img3', 'img4']


@patch('ImageDuplicateFinder.model.duplicateFinderCNN.create_dataloader')
@patch('ImageDuplicateFinder.model.duplicateFinderCNN.extract_features',
       return_value=(torch.randn(4, 512), ['img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg']))
def test_find_duplicates_cnn(mock_create_dataloader, mock_extract_features, tmpdir):
    image_dir = tmpdir.mkdir("images")

    # Create some dummy image files
    for i in range(4):
        with open(image_dir.join(f'image_{i}.jpg'), 'wb') as f:
            f.write(np.random.bytes(100))

    duplicates = find_duplicates_cnn(str(image_dir), batch_size=2, threshold=0.9)

    assert len(duplicates) == 0  # As we mocked the output, there should be no duplicates
