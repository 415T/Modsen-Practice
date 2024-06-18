from ImageDuplicateFinder.model.imageLoader import ImageLoader
from ImageDuplicateFinder.model.duplicateFinder import DuplicateFinder
from ImageDuplicateFinder.view.resultView import ResultView

class ImageController:
    def __init__(self):
        self.loader = ImageLoader()
        self.finder = DuplicateFinder()
        self.view = ResultView()

    def load_and_find_duplicates(self, folder_path: str):
        folder = self.loader.load_folder(folder_path)
        duplicates = self.finder.find_duplicates(folder)
        self.view.display_duplicates(duplicates)

    def compare_folders(self, folder1_path: str, folder2_path: str):
        folder1 = self.loader.load_folder(folder1_path)
        folder2 = self.loader.load_folder(folder2_path)
        duplicates = self.finder.compare_folders(folder1, folder2)
        self.view.display_duplicates(duplicates)
