# ImageDuplicateFinder

## Overview
ImageDuplicateFinder is a Python-based tool designed to identify duplicate images within a directory or between two directories. It provides functionality to find duplicates based on hash comparison and Convolutional Neural Network (CNN) feature extraction.

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
   - [Running the GUI](#running-the-gui)
   - [Finding Duplicates in a Folder](#finding-duplicates-in-a-folder)
   - [Comparing Two Folders for Duplicates](#comparing-two-folders-for-duplicates)
   - [Finding Duplicates Using CNN](#finding-duplicates-using-cnn)
4. [Modules](#modules)
5. [Tests](#tests)

## Features
- **Hash-based Duplicate Detection**: Quickly find duplicate images within a folder or between two folders using image hashes.
- **CNN-based Duplicate Detection**: Use a pre-trained CNN to extract features from images and find duplicates based on cosine similarity.
- **Graphical User Interface (GUI)**: A PyQt6-based GUI for easy interaction and visualization of duplicate images.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/Modsen-Practice.git
    cd Modsen-Practice/ImageDuplicateFinder
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

Ensure you have Python 3.8+ installed.

## Usage

### Running the GUI
To start the GUI, run the following command:
```bash
python main.py
```
This will open the Duplicate Image Finder application where you can select folders and find duplicate images using either hash-based or CNN-based methods.

### Finding Duplicates in a Folder
You can find duplicates within a folder using the hash-based method:
```python
from ImageDuplicateFinder.model.duplicateFinder import DuplicateFinder
from ImageDuplicateFinder.model.imageLoader import ImageLoader

folder = ImageLoader.load_folder('/path/to/images')
duplicates = DuplicateFinder.find_duplicates(folder)
print(duplicates)
```

### Comparing Two Folders for Duplicates
To compare two folders for duplicates using the hash-based method:
```python
from ImageDuplicateFinder.model.duplicateFinder import DuplicateFinder
from ImageDuplicateFinder.model.imageLoader import ImageLoader

folder1 = ImageLoader.load_folder('/path/to/first_folder')
folder2 = ImageLoader.load_folder('/path/to/second_folder')
duplicates_between_folders = DuplicateFinder.compare_folders(folder1, folder2)
print(duplicates_between_folders)
```

### Finding Duplicates Using CNN
To find duplicates within a folder using the CNN-based method:
```python
from ImageDuplicateFinder.model.duplicateFinderCNN import find_duplicates_cnn
from ImageDuplicateFinder.model.imageLoader import ImageLoader

folder = ImageLoader.load_folder('/path/to/images')
duplicates = find_duplicates_cnn(folder)
print(duplicates)
```

## Modules

### model
- **duplicateFinder.py**: Contains `DuplicateFinder` class for hash-based duplicate detection.
- **duplicateFinderCNN.py**: Contains functions for CNN-based duplicate detection.
- **image.py**: Defines the `Image` class for handling image paths and computing image hashes.
- **imageFolder.py**: Defines the `ImageFolder` class for managing image directories.
- **imageLoader.py**: Provides the `ImageLoader` class to load `ImageFolder` instances.

### tests
- **test_duplicateFinder.py**: Unit tests for the `DuplicateFinder` class.
- **test_imageFolder.py**: Unit tests for the `ImageFolder` class.
- **test_dataset.py**: Unit tests for dataset utilities.
- **test_duplicateFinderCNN.py**: Unit tests for the CNN-based duplicate detection functions.

### utils
- **dataset.py**: Utilities for handling image datasets, including custom dataset classes and dataloaders.
- **log.py**: Utility for configuring and returning a logger instance.

### view
- **mainWindow.py**: Contains the `DuplicateImageFinderGUI` class for the GUI application.

### main.py
Entry point for running the ImageDuplicateFinder GUI application.

## Tests
To run the tests, use the following command:
```bash
python -m pytest
```
This will execute all the unit tests and ensure that the application functions correctly.