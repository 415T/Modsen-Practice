from pathlib import Path
from typing import List
from image import Image

class ImageFolder:
    def __init__(self, directory: str, file_formats: List[str] = None):
        self.directory = Path(directory)
        if file_formats is None:
            self.file_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
        else:
            self.file_formats = file_formats
        self.images = self.load_images()

    def load_images(self) -> List[Image]:
        images = []
        for file_path in self.directory.rglob('*'):
            if file_path.suffix.lower() in self.file_formats:
                try:
                    image = Image(str(file_path))
                    if image.hash:
                        images.append(image)
                except Exception as e:
                    print(f"Error loading image {file_path}: {e}")
        return images
