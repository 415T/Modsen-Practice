import hashlib
from PIL import Image as PILImage

class Image:
    def __init__(self, path: str):
        self.path = path
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        try:
            with PILImage.open(self.path) as img:
                img = img.resize((256, 256)).convert('RGB')
                return hashlib.md5(img.tobytes()).hexdigest()
        except Exception as e:
            print(f"Error processing image {self.path}: {e}")
            return ""
