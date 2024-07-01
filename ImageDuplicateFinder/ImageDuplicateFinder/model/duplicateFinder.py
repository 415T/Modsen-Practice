from typing import List, Tuple, Dict
from ImageDuplicateFinder.model.image import Image
from ImageDuplicateFinder.model.imageFolder import ImageFolder
from concurrent.futures import ThreadPoolExecutor
from ImageDuplicateFinder.utils.log import return_logger

logger = return_logger(__name__)
class DuplicateFinder:
    @staticmethod
    def find_duplicates(folder: ImageFolder) -> List[Tuple[Image, Image]]:
        hash_dict: Dict[str, Image] = {}
        duplicates = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(image.compute_hash): image for image in folder.images}
            for future in futures:
                try:
                    img_hash = future.result()
                    img = futures[future]
                    if img_hash in hash_dict:
                        duplicates.append((img, hash_dict[img_hash]))
                    else:
                        hash_dict[img_hash] = img
                except Exception as e:
                    logging.error(f"Error processing image: {e}")
        return duplicates

    @staticmethod
    def compare_folders(folder1: ImageFolder, folder2: ImageFolder) -> List[Tuple[Image, Image]]:
        hash_dict: Dict[str, Image] = {image.hash: image for image in folder1.images}
        duplicates = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(image.compute_hash): image for image in folder2.images}
            for future in futures:
                try:
                    img_hash = future.result()
                    img = futures[future]
                    if img_hash in hash_dict:
                        duplicates.append((img, hash_dict[img_hash]))
                except Exception as e:
                    logging.error(f"Error processing image: {e}")
        return duplicates