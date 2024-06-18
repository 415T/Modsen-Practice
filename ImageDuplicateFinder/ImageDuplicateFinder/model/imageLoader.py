from ImageDuplicateFinder.model.imageFolder import ImageFolder

class ImageLoader:
    @staticmethod
    def load_folder(directory: str) -> ImageFolder:
        return ImageFolder(directory)
