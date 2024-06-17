import os
from PIL import Image
import numpy as np
import imagehash
import matplotlib.pyplot as plt

class ImageDuplicateFinder:
    def __init__(self, supported_formats=('jpg', 'jpeg')):
        self.supported_formats = supported_formats
        self.images = []
        self.image_paths = []
        self.hashes = []
        self.duplicates = {}

    def load_images_from_directory(self, directory):

    def calculate_hashes(self):

    def find_duplicates(self):

    def print_duplicates(self):

    def visualize_duplicates(self):

    def process_directory(self, directory):


if __name__ == '__main__':
    finder = ImageDuplicateFinder()