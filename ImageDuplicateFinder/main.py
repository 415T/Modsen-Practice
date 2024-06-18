from ImageDuplicateFinder.controller.imageController import ImageController

if __name__ == "__main__":
    controller = ImageController()

    print("Searching for duplicates in a single folder...")
    controller.load_and_find_duplicates('D:\Projects\Modsen-Practice-Git\PlantNet-300K-main\images')

    print("Comparing images between two folders...")
    controller.compare_folders('D:\Projects\Modsen-Practice-Git\PlantNet-300K-main\images', 'D:\Projects\Modsen-Practice-Git\PlantNet-300K-main\images - Copy')