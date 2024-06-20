import matplotlib.pyplot as plt
from PIL import Image as PILImage
from typing import List, Tuple
from ImageDuplicateFinder.model.image import Image

class ResultView:
    @staticmethod
    def display_and_visualize_duplicates(duplicates: List[Tuple[Image, Image]]):
        if not duplicates:
            print("No duplicates found.")
            return

        fig, axes = plt.subplots(len(duplicates), 2, figsize=(10, 5 * len(duplicates)))

        if len(duplicates) == 1:
            axes = [axes]

        for i, (img1, img2) in enumerate(duplicates):
            axes[i][0].imshow(PILImage.open(img1.path))
            axes[i][0].set_title(f"File: {img1.path.split('/')[-1]}\nPath: {img1.path}")
            axes[i][0].axis('off')

            axes[i][1].imshow(PILImage.open(img2.path))
            axes[i][1].set_title(f"File: {img2.path.split('/')[-1]}\nPath: {img2.path}")
            axes[i][1].axis('off')

        plt.tight_layout()
        plt.show()
