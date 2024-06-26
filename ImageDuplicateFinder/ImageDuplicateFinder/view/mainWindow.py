import matplotlib
matplotlib.use('QtAgg')

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QTextEdit, QScrollArea, QHBoxLayout
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PIL import Image as PILImage
from ImageDuplicateFinder.model.imageLoader import ImageLoader
from ImageDuplicateFinder.model.duplicateFinder import DuplicateFinder

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Duplicate Finder")
        self.setGeometry(100, 100, 1200, 800)

        self.loader = ImageLoader()
        self.finder = DuplicateFinder()

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.folder1_btn = QPushButton("Select Folder 1")
        self.folder1_btn.clicked.connect(self.select_folder1)
        button_layout.addWidget(self.folder1_btn)

        self.folder2_btn = QPushButton("Select Folder 2")
        self.folder2_btn.clicked.connect(self.select_folder2)
        button_layout.addWidget(self.folder2_btn)

        self.find_duplicates_btn = QPushButton("Find Duplicates in Folder 1")
        self.find_duplicates_btn.clicked.connect(self.find_duplicates)
        button_layout.addWidget(self.find_duplicates_btn)

        self.compare_folders_btn = QPushButton("Compare Folder 1 and Folder 2")
        self.compare_folders_btn.clicked.connect(self.compare_folders)
        button_layout.addWidget(self.compare_folders_btn)

        main_layout.addLayout(button_layout)

        self.results_label = QLabel("Results:")
        main_layout.addWidget(self.results_label)

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMaximumHeight(200)
        main_layout.addWidget(self.results_text)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def select_folder1(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder 1")
        if folder:
            self.folder1_path = folder
            self.folder1_btn.setText(f"Folder 1: {folder}")

    def select_folder2(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder 2")
        if folder:
            self.folder2_path = folder
            self.folder2_btn.setText(f"Folder 2: {folder}")

    def find_duplicates(self):
        if hasattr(self, 'folder1_path'):
            folder = self.loader.load_folder(self.folder1_path)
            duplicates = self.finder.find_duplicates(folder)
            self.display_results(duplicates)
        else:
            self.results_text.setText("Folder 1 is not selected.")

    def compare_folders(self):
        if hasattr(self, 'folder1_path') and hasattr(self, 'folder2_path'):
            folder1 = self.loader.load_folder(self.folder1_path)
            folder2 = self.loader.load_folder(self.folder2_path)
            duplicates = self.finder.compare_folders(folder1, folder2)
            self.display_results(duplicates)
        else:
            self.results_text.setText("One or both folders are not selected.")

    def display_results(self, duplicates):
        if duplicates:
            results = ""
            for img1, img2 in duplicates:
                results += f"Duplicate found: {img1.path} and {img2.path}\n"
            self.results_text.setText(results)
            self.visualize_duplicates(duplicates)
        else:
            self.results_text.setText("No duplicates found.")

    def visualize_duplicates(self, duplicates):
        rows = min(len(duplicates), 100)
        cols = 2

        fig, axes = plt.subplots(rows, cols, figsize=(10, 5 * rows))

        if rows == 1:
            axes = [axes]

        for i, (img1, img2) in enumerate(duplicates[:100]):
            file1_name = img1.path.split('\\')[-1]
            file2_name = img2.path.split('\\')[-1]
            path1 = img1.path
            path2 = img2.path

            axes[i][0].imshow(PILImage.open(img1.path))
            axes[i][0].axis('off')
            axes[i][0].set_title(f"File: {file1_name}\nPath: {path1}", fontsize=8, pad=20)

            axes[i][1].imshow(PILImage.open(img2.path))
            axes[i][1].axis('off')
            axes[i][1].set_title(f"File: {file2_name}\nPath: {path2}", fontsize=8, pad=20)

        plt.tight_layout()
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(5 * rows * 100)
        self.scroll_area.setWidget(canvas)
        plt.close(fig)