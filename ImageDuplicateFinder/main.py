import os
from PIL import Image
import numpy as np
import imagehash
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class ImageDuplicateFinder:
    def __init__(self, supported_formats=('jpg', 'jpeg')):
        self.supported_formats = supported_formats
        self.images = []
        self.image_paths = []
        self.hashes = []
        self.duplicates = {}

    def load_images_from_directory(self, directory):
        for filename in os.listdir(directory):
            if filename.lower().endswith(self.supported_formats):
                try:
                    image_path = os.path.join(directory, filename)
                    image = Image.open(image_path)
                    self.images.append(image)
                    self.image_paths.append(image_path)
                except Exception as e:
                    print(f"Ошибка загрузки изображения {filename}: {e}")

    def calculate_hashes(self):
        for image in self.images:
            hash_value = imagehash.average_hash(image)
            self.hashes.append(hash_value)

    def find_duplicates(self):
        hash_dict = {}
        for idx, hash_value in enumerate(self.hashes):
            if hash_value in hash_dict:
                if hash_value not in self.duplicates:
                    self.duplicates[hash_value] = [hash_dict[hash_value]]
                self.duplicates[hash_value].append(self.image_paths[idx])
            else:
                hash_dict[hash_value] = self.image_paths[idx]

    def print_duplicates(self):
        for hash_value, paths in self.duplicates.items():
            if len(paths) > 1:
                print(f"Дублирование изображений с хэшом {hash_value}:")
                for path in paths:
                    print(f"  - {path}")

    def process_directory(self, directory):
        self.load_images_from_directory(directory)
        self.calculate_hashes()
        self.find_duplicates()
        self.print_duplicates()


if __name__ == '__main__':
    directory = 'D:\Projects\Modsen-Practice-Git\PlantNet-300K-main\images'
    finder = ImageDuplicateFinder()
    finder.process_directory(directory)