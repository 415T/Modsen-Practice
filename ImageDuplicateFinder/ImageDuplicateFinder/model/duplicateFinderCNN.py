import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.utils.data import DataLoader
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from ImageDuplicateFinder.utils.dataset import create_dataloader


class FeatureExtractor(nn.Module):
    def __init__(self, model):
        super(FeatureExtractor, self).__init__()
        self.features = nn.Sequential(*list(model.children())[:-1])

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return x


def extract_features(dataloader: DataLoader, model: nn.Module, device: torch.device) -> Tuple[np.ndarray, List[str]]:
    model.eval()
    features = []
    paths = []
    with torch.no_grad():
        for images, batch_paths in dataloader:
            images = images.to(device)
            outputs = model(images)
            features.append(outputs.cpu().numpy())
            paths.extend(batch_paths)
    features = np.vstack(features)
    return features, paths


def find_duplicates_cnn(image_dir: str, batch_size: int = 32, num_workers: int = 4, threshold: float = 0.9) -> List[
    Tuple[str, str]]:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = models.resnet18(pretrained=True)
    model = FeatureExtractor(model).to(device)

    dataloader = create_dataloader(image_dir, batch_size, num_workers)

    features, paths = extract_features(dataloader, model, device)

    similarities = cosine_similarity(features)
    duplicates = []

    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            if similarities[i, j] > threshold:
                duplicates.append((paths[i], paths[j]))

    return duplicates
