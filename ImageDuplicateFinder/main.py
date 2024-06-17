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


if __name__ == '__main__':
    finder = ImageDuplicateFinder()