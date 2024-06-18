import matplotlib.pyplot as plt
from typing import List, Tuple
from ..model.image import Image
from PIL import Image as PILImage

class ResultView:
    @staticmethod
    def display_duplicates(duplicates: List[Tuple[Image, Image]]):
        for img1, img2 in duplicates:
            print(f"Duplicate found: {img1.path} and {img2.path}")

    @staticmethod
    def visualize_duplicates(duplicates: List[Tuple[Image, Image]]):
        for img1, img2 in duplicates:
            fig, axes = plt.subplots(1, 2)
            axes[0].imshow(PILImage.open(img1.path))
            axes[0].set_title(img1.path)
            axes[1].imshow(PILImage.open(img2.path))
            axes[1].set_title(img2.path)
            plt.show()
