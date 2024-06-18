from typing import List, Tuple, Dict
from image import Image
from imageFolder import ImageFolder

class DuplicateFinder:
    @staticmethod
    def find_duplicates(folder: ImageFolder) -> List[Tuple[Image, Image]]:
        hash_dict: Dict[str, Image] = {}
        duplicates = []
        for image in folder.images:
            if image.hash in hash_dict:
                duplicates.append((image, hash_dict[image.hash]))
            else:
                hash_dict[image.hash] = image
        return duplicates

    @staticmethod
    def compare_folders(folder1: ImageFolder, folder2: ImageFolder) -> List[Tuple[Image, Image]]:
        hash_dict: Dict[str, Image] = {image.hash: image for image in folder1.images}
        duplicates = []
        for image in folder2.images:
            if image.hash in hash_dict:
                duplicates.append((image, hash_dict[image.hash]))
        return duplicates
