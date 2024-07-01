import os
from typing import List, Tuple
from PIL import Image
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
import torch

class CustomImageDataset(Dataset):
    def __init__(self, image_dir: str, transform=None):
        self.image_dir = image_dir
        self.transform = transform
        self.image_paths = self._load_image_paths()

    def _load_image_paths(self) -> List[str]:
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        return [
            os.path.join(self.image_dir, fname)
            for fname in os.listdir(self.image_dir)
            if fname.lower().endswith(valid_extensions)
        ]

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, str]:
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, img_path

def create_dataloader(image_dir: str, batch_size: int, num_workers: int = 4, transform=None) -> DataLoader:
    if transform is None:
        transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor()
        ])
    dataset = CustomImageDataset(image_dir, transform=transform)
    return DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

def filter_invalid_images(batch: List[Tuple[torch.Tensor, str]]) -> List[Tuple[torch.Tensor, str]]:
    valid_images = []
    for image, path in batch:
        if image is not None:
            valid_images.append((image, path))
        else:
            print(f"Invalid image: {path}")
    return valid_images